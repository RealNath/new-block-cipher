from cipher.algorithm import NewBlockCipher
from cipher.modes import ECBMode

if __name__ == "__main__":
    # Penggunaan ECBMode dengan algoritma NewBlockCipher
    master_key = input("Masukkan master key (8 karakter): ").encode('utf-8')
    cipher = NewBlockCipher(master_key)
    ecb_mode = ECBMode(cipher)
    while True:
        menu = """
        Pilih mode operasi (ECB):
        1. Enkripsi
        2. Dekripsi
        3. Keluar
        """
        print(menu)
        option = input("Masukkan pilihan (1/2/3): ")
        if option == "1":
                plaintext = input("Masukkan plaintext (utf-8): ").encode('utf-8')
                ciphertext = ecb_mode.encrypt(plaintext)
                ciphertext_hex = ciphertext.hex()
                print("Ciphertext (hex):", ciphertext_hex)
        elif option == "2":
                ciphertext_hex = input("Masukkan ciphertext (hex): ")
                ciphertext = bytes.fromhex(ciphertext_hex)
                decrypted_text = ecb_mode.decrypt(ciphertext)
                print("Decrypted text:", decrypted_text.decode('utf-8'))
        elif option == "3":
                print("Keluar dari program.")
                break
        else:
                print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")