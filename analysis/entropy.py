BITS_PER_BYTE = 8 # Panjang bit dalam satu byte

# Perhitungan derajat keacakan byte ciphertext
def calculate_entropy(ciphertext):
    if not ciphertext:
        raise ValueError("Ciphertext tidak boleh kosong.")

    # Menghitung frekuensi kemunculan setiap byte dalam ciphertext
    byte_frequencies = {}
    for byte in ciphertext:
        if byte in byte_frequencies:
            byte_frequencies[byte] += 1
        else:
            byte_frequencies[byte] = 1

    # Menghitung total jumlah byte dalam ciphertext
    total_bytes = len(ciphertext)

    # Menghitung entropi menggunakan rumus Shannon
    entropy = 0.0
    for frequency in byte_frequencies.values():
        probability = frequency / total_bytes
        probability_log = probability * (probability and (probability).bit_length() or 0)
        entropy -= probability_log

    return entropy

# Perhitungan entropi dalam bit per byte
def calculate_entropy_in_bits_per_byte(ciphertext):
    entropy = calculate_entropy(ciphertext)
    return entropy * BITS_PER_BYTE # Mengonversi entropi ke bit per byte