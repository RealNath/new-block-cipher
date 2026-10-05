# S-Box 4 bit
SBOX = [3, 13, 10, 11, 8, 15, 4, 5,
        6, 9, 2, 7, 0, 1, 14, 12]

# P-Box 64 bit
PBOX = [16, 8, 13, 62, 15, 11, 4, 50,
        48, 31, 35, 36, 39, 56, 49, 10,
        47, 21, 57, 29, 6, 37, 0, 46,
        41, 59, 7, 26, 24, 14, 2, 1,
        33, 23, 17, 61, 19, 45, 44, 52,
        43, 58, 30, 60, 5, 27, 34, 51,
        63, 42, 28, 40, 22, 12, 20, 32,
        18, 9, 53, 38, 25, 3, 55, 54]

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

# Rotasi binary ke kiri sebanyak shift_amount
def circular_shift(value, shift_amount):
    shift_amount %= 64
    shifted =  (value << shift_amount) | (value >> (64 - shift_amount))
    # Masking, karena "value << shift_amount" tidak membuang shift_amount bit terkiri
    mask = 0xFFFFFFFFFFFFFFFF # 64 angka "1" dlm binary
    return shifted & mask