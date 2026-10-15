# New Block Cipher (NBC-64)

Implementasi algoritma cipher blok simetris berbasis Jaringan Feistel 16 putaran, dengan ukuran dan kunci 64 bit. Program ini mendukung 5 mode operasi cipher blok ECB, CBC, CFB, OFB, CTR, dengan skema padding PKCS#7, enkripsi/dekripsi teks dan file binary sembarang, serta avalanche effect, entropi Shannon, dan histogram frekuensi byte untuk analisis.

---

## 1. Deskripsi Program & Algoritma

Program ini merupakan implementasi from scratch dari algoritma cipher blok tanpa menggunakan library kriptografi.

* Ukuran Blok: 64 bit (8 byte)
* Ukuran Kunci: 64 bit (8 byte) master key.
* Arsitektur: Jaringan Feistel, 16 putaran.
* Fungsi Putaran (F-function):
  1. Key Mixing: XOR dengan round key 32 bit (R_i XOR K_i).
  2. Confusion: Substitusi 8 nibble menggunakan S-Box 4-bit non-linear.
  3. Diffusion: Permutasi bit 32-bit (P-Box).
  4. Operasi Tambahan: Rotasi bit melingkar ke kiri sebesar 3 bit (circular left shift).
* Key Schedule: Pembangkitan 16 round key (masing-masing 32 bit) dari master key 64 bit dengan golden ratio dan rotasi dinamis.
* Mode Operasi: Mendukung 5 mode operasi standar:
  * ECB (Electronic Codebook)
  * CBC (Cipher Block Chaining)
  * CFB (Cipher Feedback)
  * OFB (Output Feedback)
  * CTR (Counter Mode)
* Padding: Skema PKCS#7 untuk penanganan data yang panjangnya bukan kelipatan ukuran blok (8 byte).
* Fitur Tambahan: Enkripsi/dekripsi berkas sembarang (teks maupun biner/gambar) serta modul analisis statistik keamanan (Avalanche Effect, Entropi Shannon, dan Histogram Distribusi).

---

## 2. Tech Stack

* Python
* CLI, terminal interaktif
* Matplotlib (visualisasi histogram)

---

## 3. Dependensi

Program inti cipher blok dan seluruh mode operasinya diimplementasikan murni menggunakan library bawaan standar Python tanpa library external. Dependensi external hanya untuk visualisasi histogram:

* matplotlib (visualisasi modul analisis `analysis/histogram.py`)

Installation dependensi: (lihat bagian 4)

---

## 4. Tata Cara Menjalankan Program


1. (Opsional) Pakai virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux
   # venv\Scripts\activate     # Windows
   ```
2. Install dependensi:
   ```bash
   pip install matplotlib
   ```

3. Jalankan app.py melalui terminal:
    ```bash
    python3 app.py
    ```

Alur penggunaan program:
1. Masukkan Master Key 8 karakter (64 bit).
2. Pilih salah satu mode (ECB, CBC, CFB, OFB, CTR).
3. Jika memilih CBC/CFB/OFB, masukkan IV (Initialization Vector) 8 karakter. Jika CTR, masukkan Nonce 4 karakter.
4. Pilih menu operasi yang diinginkan:
   * Enkripsi teks: Masukkan string plaintext UTF-8, program akan menghasilkan ciphertext dalam representasi heksadesimal.
   * Dekripsi teks: Masukkan ciphertext heksadesimal, program akan mengembalikan plaintext semula.
   * Enkripsi file: Letakkan file target dalam folder `files/`, masukkan nama file (misal `sample.png` atau `document.txt`). File hasil enkripsi akan disimpan dengan sufiks `_encrypted`.
   * Dekripsi file: Masukkan nama file terenkripsi dari folder `files/`. File akan didekripsi dan diverifikasi integritas padding-nya.

### Analisis Keamanan
Modul pengujian pada folder `analysis/` dapat dijalankan atau diimpor untuk mengevaluasi cipher:
* Pengujian Avalanche Effect:
  ```python
  from analysis.avalanche import calculate_avalanche_effect
  # Menghitung persentase perbedaan bit antara 2 ciphertext
  ```
* Pengujian Entropi Shannon:
  ```python
  from analysis.entropy import calculate_entropy_in_bits_per_byte
  # Menghitung derajat keacakan byte ciphertext (maksimal 8.0 bit/byte)
  ```
* Visualisasi Histogram:
  ```python
  from analysis.histogram import plot_comparison_histograms
  plot_comparison_histograms(plaintext_bytes, ciphertext_bytes)
  ```