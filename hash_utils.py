"""
Hash utilities for extensible hashing operations
Funciones auxiliares para operaciones de hash extensible
"""

def get_hash_bits(key, depth):
    # Obtiene los últimos 'depth' bits del hash de la clave
    return key & ((1 << depth) - 1)


def format_binary_address(index, depth):
    # Formatea un índice como dirección binaria con padding
    return bin(index)[2:].zfill(depth)


def calculate_buddy_index(index, local_depth):
    # Calcula el índice del bucket buddy para operaciones de merge
    # Alternar el bit más significativo de la profundidad local
    buddy_bit = 1 << (local_depth - 1)
    return index ^ buddy_bit


def should_split_to_new_bucket(key, local_depth):
    # Determina si una clave debe ir al nuevo bucket después de una división
    return bool(get_hash_bits(key, local_depth) & 1)
