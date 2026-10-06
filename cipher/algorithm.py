BLOCK_SIZE = 8 # 64 bits (8 bytes)
KEY_SIZE = 8 # 64 bits (8 bytes)
ROUND_COUNT = 16 # iterated cipher 16 rounds

# S-Box 4 bit
SBOX = [3, 13, 10, 11, 8, 15, 4, 5,
        6, 9, 2, 7, 0, 1, 14, 12]

# P-Box 32 bit (feistel, masing-masing kiri dan kanan 32 bit)
PBOX = [25, 31, 20, 11, 9, 4, 18, 1,
        17, 6, 29, 16, 28, 15, 2, 0,
        23, 13, 12, 22, 19, 24, 30, 21,
        5, 14, 26, 27, 10, 7, 3, 8]

def apply_sbox(value_32bit):
    result = 0
    for i in range(8):
        # Ambil per 4 bit, dari kanan
        chunk = (value_32bit >> (i * 4)) & 0b1111
        substitution = SBOX[chunk]
        result = result | (substitution << (i * 4))
    return result

# Pindahkan bit ke-i ke posisi ke-PBOX[i]
def apply_pbox(value):
    result = 0
    for i in range(len(PBOX)):
        # Get bit of position i
        # "value >> i" bikin bit ke-i jadi paling kanan
        # "& 1" ambil bit terakhir dari hasil "value >> i"
        bit = (value >> i) & 1

        new_pos = PBOX[i]
        result = result | (bit << new_pos)
    return result

# Rotasi binary ke kiri sebanyak shift_amount sebanyak 32 bit (karena setengah kiri dan kanan masing-masing 32 bit)
def circular_shift_32(value, shift_amount):
    shift_amount %= 32
    shifted =  (value << shift_amount) | (value >> (32 - shift_amount))
    # Masking, karena "value << shift_amount" tidak membuang shift_amount bit terkiri
    mask = 0xFFFFFFFF # singkatan 32 angka "1" (0b111...111) dlm binary
    return shifted & mask

def f_function(right_half, round_key):
    ri_xor_ki = right_half ^ round_key
    substitution = apply_sbox(ri_xor_ki)
    permutation = apply_pbox(substitution)
    result = circular_shift_32(permutation, 3)
    return result

# Jaringan Feistel (iterated cipher 16 round)
def encrypt_block(block_64bit, round_keys):
    l_i = block_64bit >> 32
    r_i = block_64bit & 0xFFFFFFFF # singkatan 32 angka "1" (0b111...111) dlm binary

    for i in range(ROUND_COUNT):
        key = round_keys[i]
        
        # Jaringan Feistel
        l_i_plus_1 = r_i
            # R_i+1 = L_i XOR f(R_i, K_i)
        r_i_plus_1 = l_i ^ f_function(r_i, key)
        
        l_i = l_i_plus_1
        r_i = r_i_plus_1
    
    result = (r_i << 32) | l_i
    return result

def decrypt_block(block_64bit, round_keys):
    r_i = block_64bit >> 32
    l_i = block_64bit & 0xFFFFFFFF # singkatan 32 angka "1" (0b111...111) dlm binary

    for i in range(ROUND_COUNT - 1, -1, -1):
        key = round_keys[i]
        
        # Jaringan Feistel
        r_i_minus_1 = l_i
            # L_i+1 = R_i XOR f(L_i, K_i)
        l_i_minus_1 = r_i ^ f_function(l_i, key)
        
        r_i = r_i_minus_1
        l_i = l_i_minus_1

    result = (l_i << 32) | r_i
    return result