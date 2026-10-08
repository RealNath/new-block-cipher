from .modes import CipherMode

class FileCipher:

    @staticmethod
    def encrypt_file(cipher_mode : CipherMode, input_file_path, output_file_path):
        with open(input_file_path, 'rb') as input_file:
            plaintext = input_file.read()
            ciphertext = cipher_mode.encrypt(plaintext)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(ciphertext)

    @staticmethod
    def decrypt_file(cipher_mode : CipherMode, input_file_path, output_file_path):
        with open(input_file_path, 'rb') as input_file:
            ciphertext = input_file.read()
            plaintext = cipher_mode.decrypt(ciphertext)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(plaintext)