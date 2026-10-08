from cipher.algorithm import NewBlockCipher
from cipher.modes import ECBMode, CBCMode, CFBMode, OFBMode, CTRMode
from cipher.file_cipher import FileCipher

if __name__ == "__main__":
    # Penggunaan ECBMode dengan algoritma NewBlockCipher
    print("=== New Block Cipher ===")
    print("Aplikasi block cipher sederhana dengan berbagai mode operasi.\n\n")
    master_key = input("Masukkan kunci cipher (8 karakter): ").encode('utf-8')
    cipher = NewBlockCipher(master_key)
    mode_option = input("""
        Pilih mode operasi:
        1. ECB (Electronic Codebook)
        2. CBC (Cipher Block Chaining)
        3. CFB (Cipher Feedback)
        4. OFB (Output Feedback)
        5. CTR (Counter)
        6. Exit
        """)
    match mode_option:
        case "1":
                cipher_mode = ECBMode(cipher)
        case "2":
                iv = input("Masukkan initial vector (string 8 karakter): ").encode('utf-8')
                cipher_mode = CBCMode(cipher, iv)
        case "3":
                iv = input("Masukkan initial vector (string 8 karakter): ").encode('utf-8')
                cipher_mode = CFBMode(cipher, iv)
        case "4":
                iv = input("Masukkan initial vector (string 8 karakter): ").encode('utf-8')
                cipher_mode = OFBMode(cipher, iv)
        case "5":
                nonce = input("Masukkan nonce (string 4 karakter): ").encode('utf-8')
                cipher_mode = CTRMode(cipher, nonce)
        case "6":
                print("Keluar dari program.")
                exit()
        case _:
                print("Pilihan tidak valid. Silakan pilih 1, 2, 3, 4, 5, atau 6.")
                exit()

    while True:
        menu = """
        Pilih mode operasi (ECB):
        1. Enkripsi teks
        2. Dekripsi teks
        3. Enkripsi file
        4. Dekripsi file
        5. Keluar
        """
        print(menu)
        option = input("Masukkan pilihan (1/2/3): ")
        if option == "1":
                plaintext = input("Masukkan plaintext (utf-8): ").encode('utf-8')
                ciphertext = cipher_mode.encrypt(plaintext)
                ciphertext_hex = ciphertext.hex()
                print("Ciphertext (hex):", ciphertext_hex)
        elif option == "2":
                ciphertext_hex = input("Masukkan ciphertext (hex): ")
                ciphertext = bytes.fromhex(ciphertext_hex)
                decrypted_text = cipher_mode.decrypt(ciphertext)
                print("Decrypted text:", decrypted_text.decode('utf-8'))
        elif option == "3":
                input_file_name = input("Masukkan nama file di folder files (contoh: plaintext.txt): ")
                input_file_path = "files/" + input_file_name

                output_file_name = input_file_name.split('.')[0] + "_encrypted." + input_file_name.split('.')[1]
                output_file_path = "files/" + output_file_name

                FileCipher.encrypt_file(cipher_mode, input_file_path, output_file_path)
                print(f"File terenkripsi disimpan di: {output_file_path}")
        elif option == "4":
                input_file_name = input("Masukkan nama file terenkripsi di folder files (contoh: ciphertext.txt): ")
                input_file_path = "files/" + input_file_name

                output_file_name = input_file_name.split('_')[0] + "_decrypted." + input_file_name.split('.')[1]
                output_file_path = "files/" + output_file_name

                FileCipher.decrypt_file(cipher_mode, input_file_path, output_file_path)
                print(f"File terdekripsi disimpan di: {output_file_path}")
        elif option == "5":
                print("Keluar dari program.")
                break
        else:
                print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")