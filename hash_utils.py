"""
Funciones auxiliares para operaciones de hash extensible
"""

def get_hash_bits(key, depth):
    # Obtiene los ultimos depth bits del hash de la clave
    return key & ((1 << depth) - 1)


def format_binary_address(index, depth):
    # Formatea un índice como dirección binaria con padding
    return bin(index)[2:].zfill(depth)


def calculate_buddy_index(index, local_depth):
    # Calcula el índice del bucket buddy para operaciones de merge
    # Alternar el bit más significativo de la profundidad local
    buddy_bit = 1 << (local_depth - 1)
    return index ^ buddy_bit


def should_split_to_new_bucket(key, new_local_depth):
    # Determina si una clave debe ir al nuevo bucket después de una división
    # Usar el bit más significativo de la nueva profundidad local
    hash_bits = get_hash_bits(key, new_local_depth)
    # El bit que diferencia es el de posición (new_local_depth - 1)
    distinguishing_bit = 1 << (new_local_depth - 1)
    return bool(hash_bits & distinguishing_bit)
