"""
Directorio que mantiene punteros a buckets y maneja la profundidad global
"""


from bucket import Bucket
from hash_utils import get_hash_bits, format_binary_address
from config import INITIAL_GLOBAL_DEPTH, MINIMUM_GLOBAL_DEPTH, INITIAL_LOCAL_DEPTH, MIN_KEY_VALUE, MAX_KEY_VALUE


class Directory:
    
    def __init__(self):
        self.global_depth = INITIAL_GLOBAL_DEPTH
        self.buckets = []
        self.directory = []
        
        # Inicializar con 4 buckets (2^2) cada uno con profundidad local 2
        for i in range(2 ** INITIAL_GLOBAL_DEPTH):
            bucket = Bucket(local_depth=INITIAL_LOCAL_DEPTH)
            self.buckets.append(bucket)
            self.directory.append(i)
    
    def _get_bucket_index(self, key):
        # Calcula el índice del directorio usando los últimos global_depth bits
        return get_hash_bits(key, self.global_depth)
    
    def _get_bucket(self, key):
        # Obtiene el bucket correspondiente a una clave
        dir_index = self._get_bucket_index(key)
        bucket_id = self.directory[dir_index]
        return self.buckets[bucket_id], bucket_id
    
    def search(self, key):
        # Busca una clave en el índice
        bucket, _ = self._get_bucket(key)
        return bucket.contains(key)
    
    def insert(self, key):
        # Inserta una clave en el índice
        if not (MIN_KEY_VALUE <= key <= MAX_KEY_VALUE):
            return False, f"Clave debe estar entre {MIN_KEY_VALUE} y {MAX_KEY_VALUE}"
        
        bucket, bucket_id = self._get_bucket(key)
        
        # Si la clave ya existe
        if bucket.contains(key):
            return False, f"Clave {key} ya existe"
        
        # Si el bucket no está lleno, insertar directamente
        if bucket.insert(key):
            return True, f"Clave {key} insertada exitosamente"
        
        # Bucket está lleno, necesita división
        return self._handle_overflow(key, bucket_id)
    
    def _handle_overflow(self, key, bucket_id):
        # Maneja el desbordamiento de un bucket mediante división
        bucket = self.buckets[bucket_id]
        
        # Si local_depth == global_depth, doblar el directorio primero
        if bucket.local_depth == self.global_depth:
            self._double_directory()
        
        # Dividir el bucket
        new_bucket = bucket.split()
        new_bucket_id = len(self.buckets)
        self.buckets.append(new_bucket)
        
        # Actualizar punteros del directorio
        self._update_directory_pointers(bucket_id, new_bucket_id)
        
        # Intentar insertar la clave nuevamente
        bucket, _ = self._get_bucket(key)
        print(bucket)
        if bucket.insert(key):
            return True, f"Clave {key} insertada después de división de bucket"
        else:
            return False, "Error: No se pudo insertar después de la división"
    
    def _double_directory(self):
        # Dobla el tamaño del directorio incrementando la profundidad global
        self.global_depth += 1
        # Duplicar entradas existentes
        self.directory = self.directory + self.directory.copy()
    
    def _update_directory_pointers(self, old_bucket_id, new_bucket_id):
        # Actualiza los punteros del directorio después de una división
        old_bucket = self.buckets[old_bucket_id]
        
        for i in range(len(self.directory)):
            if self.directory[i] == old_bucket_id:
                # Verificar si esta entrada debe apuntar al nuevo bucket
                if self._should_point_to_new_bucket(i, old_bucket.local_depth):
                    self.directory[i] = new_bucket_id
    
    def _should_point_to_new_bucket(self, dir_index, local_depth):
        # Determina si una entrada del directorio debe apuntar al nuevo bucket
        # Usar el bit de profundidad local para decidir
        return (dir_index >> (local_depth - 1)) & 1
    
    def delete(self, key):
        # Elimina una clave del índice
        bucket, bucket_id = self._get_bucket(key)
        
        if not bucket.delete(key):
            return False, f"Clave {key} no encontrada"
        
        # Verificar si es necesario fusionar buckets
        self._check_merge(bucket_id)
        
        # Verificar si es posible reducir el directorio
        self._check_shrink_directory()
        
        return True, f"Clave {key} eliminada exitosamente"
    
    def _check_merge(self, bucket_id):
        # Verifica si un bucket puede fusionarse con su buddy
        bucket = self.buckets[bucket_id]
        
        if bucket.is_empty() and bucket.local_depth > 1:
            # Encontrar el buddy bucket
            buddy_id = self._find_buddy_bucket(bucket_id)
            if buddy_id is not None:
                buddy = self.buckets[buddy_id]
                
                # Si ambos buckets pueden fusionarse
                if (buddy.local_depth == bucket.local_depth and 
                    len(buddy.keys) + len(bucket.keys) <= buddy.max_size):
                    self._merge_buckets(bucket_id, buddy_id)
    
    def _find_buddy_bucket(self, bucket_id):
        # Encuentra el bucket buddy para fusión
        bucket = self.buckets[bucket_id]
        
        for i, other_bucket in enumerate(self.buckets):
            if (i != bucket_id and 
                other_bucket.local_depth == bucket.local_depth):
                return i
        return None
    
    def _merge_buckets(self, bucket_id1, bucket_id2):
        # Fusiona dos buckets
        bucket1 = self.buckets[bucket_id1]
        bucket2 = self.buckets[bucket_id2]
        
        # Fusionar claves en bucket1
        bucket1.keys.extend(bucket2.keys)
        bucket1.keys.sort()
        bucket1.local_depth -= 1
        
        # Actualizar punteros del directorio
        for i in range(len(self.directory)):
            if self.directory[i] == bucket_id2:
                self.directory[i] = bucket_id1
        
        # Marcar bucket2 como no utilizado (no lo eliminamos para mantener IDs)
        bucket2.keys = []
    
    def _check_shrink_directory(self):
        # Verifica si el directorio puede reducirse
        if self.global_depth <= MINIMUM_GLOBAL_DEPTH:
            return
        
        # Verificar si todas las entradas en pares apuntan al mismo bucket
        can_shrink = True
        half_size = len(self.directory) // 2
        
        for i in range(half_size):
            if self.directory[i] != self.directory[i + half_size]:
                can_shrink = False
                break
        
        if can_shrink:
            self.global_depth -= 1
            self.directory = self.directory[:half_size]
    
    def print_status(self):
        # Imprime el estado actual del índice
        print(f"\n=== Estado del Índice Hash Extensible ===")
        print(f"Profundidad Global: {self.global_depth}")
        print(f"Tamaño del Directorio: {len(self.directory)}")
        
        print(f"\nDirectorio:")
        for i, bucket_id in enumerate(self.directory):
            binary_addr = format_binary_address(i, self.global_depth)
            print(f"  {binary_addr} → Bucket {bucket_id}")
        
        print(f"\nBuckets:")
        for i, bucket in enumerate(self.buckets):
            if not bucket.is_empty() or any(self.directory[j] == i for j in range(len(self.directory))):
                print(f"  Bucket {i}: {bucket}")
        print("=" * 45)
