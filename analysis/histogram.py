import matplotlib.pyplot as plt

# Perhitungan histogram byte dalam data
def calculate_histogram(data):
    if not data:
        raise ValueError("Data tidak boleh kosong.")

    # Menghitung frekuensi kemunculan setiap byte dalam data
    byte_frequencies = {}
    for byte in data:
        if byte in byte_frequencies:
            byte_frequencies[byte] += 1
        else:
            byte_frequencies[byte] = 1

    return byte_frequencies

# Perbandingan histogram antara plaintext dan ciphertext
def compare_histograms(plaintext, ciphertext):
    if not plaintext or not ciphertext:
        raise ValueError("Plaintext dan ciphertext tidak boleh kosong.")

    # Menghitung histogram untuk plaintext dan ciphertext
    plaintext_histogram = calculate_histogram(plaintext)
    ciphertext_histogram = calculate_histogram(ciphertext)

    return plaintext_histogram, ciphertext_histogram

# Perbandingan histogram antara plaintext dan ciphertext dalam bentuk grafik
def plot_comparison_histograms(plaintext, ciphertext):
    if not plaintext or not ciphertext:
        raise ValueError("Plaintext dan ciphertext tidak boleh kosong.")

    # Menghitung histogram untuk plaintext dan ciphertext
    plaintext_histogram, ciphertext_histogram = compare_histograms(plaintext, ciphertext)

    # Menampilkan histogram dalam bentuk grafik
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.bar(plaintext_histogram.keys(), plaintext_histogram.values())
    plt.xlabel('Nilai Byte')
    plt.ylabel('Frekuensi')
    plt.title('Plaintext Histogram')

    plt.subplot(1, 2, 2)
    plt.bar(ciphertext_histogram.keys(), ciphertext_histogram.values())
    plt.xlabel('Nilai Byte')
    plt.ylabel('Frekuensi')
    plt.title('Ciphertext Histogram')

    plt.tight_layout()
    plt.show()

# Perhitungan keseragaman distribusi histogram
def calculate_uniformity(histogram):
    if not histogram:
        raise ValueError("Histogram tidak boleh kosong.")

    # Menghitung total jumlah byte dalam histogram
    total_bytes = sum(histogram.values())

    # Menghitung keseragaman distribusi histogram
    uniformity = 0.0
    for frequency in histogram.values():
        probability = frequency / total_bytes
        uniformity += probability ** 2

    return uniformity

# Perbandingan keseragaman distribusi histogram antara plaintext dan ciphertext
def compare_uniformity(plaintext, ciphertext):
    if not plaintext or not ciphertext:
        raise ValueError("Plaintext dan ciphertext tidak boleh kosong.")

    # Menghitung histogram untuk plaintext dan ciphertext
    plaintext_histogram, ciphertext_histogram = compare_histograms(plaintext, ciphertext)

    # Menghitung keseragaman distribusi histogram untuk plaintext dan ciphertext
    plaintext_uniformity = calculate_uniformity(plaintext_histogram)
    ciphertext_uniformity = calculate_uniformity(ciphertext_histogram)

    return plaintext_uniformity, ciphertext_uniformity