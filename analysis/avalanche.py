BIT_LENGTH = 8 # Panjang bit dalam satu byte

# Perhitungan persentase perubahan bit antara ciphertext asli dan ciphertext yang dimodifikasi
def calculate_avalanche_effect(original_ciphertext, modified_ciphertext):
    if len(original_ciphertext) != len(modified_ciphertext):
        raise ValueError("Ciphertext asli dan ciphertext yang dimodifikasi harus memiliki panjang yang sama.")

    # Menghitung jumlah bit yang berbeda
    differing_bits = 0
    for b1, b2 in zip(original_ciphertext, modified_ciphertext):
        differing_bits += bin(b1 ^ b2).count('1')

    # Menghitung total jumlah bit
    total_bits = len(original_ciphertext) * BIT_LENGTH
    
    # Menghitung persentase perubahan bit
    avalanche_effect_percentage = (differing_bits / total_bits) * 100
    
    return avalanche_effect_percentage