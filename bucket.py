"""
Bucket class for extensible hashing implementation
Represents a bucket/page with capacity and local depth management
"""

from hash_utils import get_hash_bits, should_split_to_new_bucket
from config import BUCKET_MAX_SIZE, INITIAL_LOCAL_DEPTH


class Bucket:
    
    def __init__(self, local_depth=INITIAL_LOCAL_DEPTH):
        self.local_depth = local_depth
        self.keys = []  # Lista de claves enteras
        self.max_size = BUCKET_MAX_SIZE  # Capacidad máxima del bucket
    
    def is_full(self):
        # Verifica si el bucket está lleno
        return len(self.keys) >= self.max_size
    
    def is_empty(self):
        # Verifica si el bucket está vacío
        return len(self.keys) == 0
    
    def insert(self, key):
        # Inserta una clave si hay espacio y no existe
        if key not in self.keys and not self.is_full():
            self.keys.append(key)
            self.keys.sort()  # Mantener ordenado para mejor visualización
            return True
        return False
    
    def delete(self, key):
        # Elimina una clave si existe
        if key in self.keys:
            self.keys.remove(key)
            return True
        return False
    
    def contains(self, key):
        # Verifica si la clave existe en el bucket
        return key in self.keys
    
    def split(self):
        # Divide el bucket creando uno nuevo con mayor profundidad local
        new_bucket = Bucket(self.local_depth + 1)
        self.local_depth += 1
        
        # Redistribuir claves basado en el nuevo bit de profundidad
        remaining_keys = []
        for key in self.keys:
            # Usar el bit adicional para decidir qué bucket debe contener la clave
            if should_split_to_new_bucket(key, self.local_depth):
                new_bucket.keys.append(key)
            else:
                remaining_keys.append(key)
        
        self.keys = remaining_keys
        new_bucket.keys.sort()
        self.keys.sort()
        
        return new_bucket
    
    def __str__(self):
        return f"[{', '.join(map(str, self.keys))}] (local_depth: {self.local_depth})"
