from .algorithm import NewBlockCipher
from .padding import PKCS7Padding

class CipherMode:
    def __init__(self, cipher : NewBlockCipher):
        self.cipher = cipher

    def encrypt(self, plaintext):
        raise NotImplementedError("Metode encrypt harus diimplementasikan oleh subclass.")

    def decrypt(self, ciphertext):
        raise NotImplementedError("Metode decrypt harus diimplementasikan oleh subclass.")

class ECBMode(CipherMode):
    def encrypt(self, plaintext):
        # Memastikan panjang plaintext adalah kelipatan dari ukuran blok
        padded_plaintext = PKCS7Padding.pad(plaintext, self.cipher.block_size)
        ciphertext = b''

        for i in range(0, len(padded_plaintext), self.cipher.block_size):
            block = padded_plaintext[i:i + self.cipher.block_size]
            encrypted_block = self.cipher.encrypt_block_bytes(block)
            ciphertext += encrypted_block

        return ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) % self.cipher.block_size != 0:
            raise ValueError("Panjang ciphertext harus kelipatan dari ukuran blok.")

        decrypted_data = b''

        for i in range(0, len(ciphertext), self.cipher.block_size):
            block = ciphertext[i:i + self.cipher.block_size]
            decrypted_block = self.cipher.decrypt_block_bytes(block)
            decrypted_data += decrypted_block

        unpadded_data = PKCS7Padding.unpad(decrypted_data)
        return unpadded_data

class CBCMode(CipherMode):
    def __init__(self, cipher : NewBlockCipher, iv):
        super().__init__(cipher)
        if len(iv) != self.cipher.block_size:
            raise ValueError(f"IV harus berukuran {self.cipher.block_size} bytes.")
        self.iv = iv

    def encrypt(self, plaintext):
        padded_plaintext = PKCS7Padding.pad(plaintext, self.cipher.block_size)
        ciphertext = b''
        previous_block = self.iv

        for i in range(0, len(padded_plaintext), self.cipher.block_size):
            block = padded_plaintext[i:i + self.cipher.block_size]
            # XOR dengan blok sebelumnya (atau IV untuk blok pertama)
            block_to_encrypt = bytes(a ^ b for a, b in zip(block, previous_block))
            encrypted_block = self.cipher.encrypt_block_bytes(block_to_encrypt)
            ciphertext += encrypted_block
            previous_block = encrypted_block

        return ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) % self.cipher.block_size != 0:
            raise ValueError("Panjang ciphertext harus kelipatan dari ukuran blok.")

        decrypted_data = b''
        previous_block = self.iv

        for i in range(0, len(ciphertext), self.cipher.block_size):
            block = ciphertext[i:i + self.cipher.block_size]
            decrypted_block = self.cipher.decrypt_block_bytes(block)
            # XOR dengan blok sebelumnya (IV untuk blok pertama)
            original_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
            decrypted_data += original_block
            previous_block = block

        unpadded_data = PKCS7Padding.unpad(decrypted_data)
        return unpadded_data

class CFBMode(CipherMode):
    def __init__(self, cipher : NewBlockCipher, iv):
        super().__init__(cipher)
        if len(iv) != self.cipher.block_size:
            raise ValueError(f"IV harus berukuran {self.cipher.block_size} bytes.")
        self.iv = iv

    def encrypt(self, plaintext):
        padded_plaintext = PKCS7Padding.pad(plaintext, self.cipher.block_size)
        ciphertext = b''
        feedback = self.iv

        for i in range(0, len(padded_plaintext), self.cipher.block_size):
            block = padded_plaintext[i:i + self.cipher.block_size]
            # Enkripsi feedback
            encrypted_feedback = self.cipher.encrypt_block_bytes(feedback)
            # XOR dengan blok plaintext
            encrypted_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
            ciphertext += encrypted_block
            feedback = encrypted_block  # Update feedback dengan blok ciphertext yang baru

        return ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) % self.cipher.block_size != 0:
            raise ValueError("Panjang ciphertext harus kelipatan dari ukuran blok.")

        decrypted_data = b''
        feedback = self.iv

        for i in range(0, len(ciphertext), self.cipher.block_size):
            block = ciphertext[i:i + self.cipher.block_size]
            # Enkripsi feedback
            encrypted_feedback = self.cipher.encrypt_block_bytes(feedback)
            # XOR dengan blok ciphertext
            original_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
            decrypted_data += original_block
            feedback = block  # Update feedback dengan blok ciphertext yang baru

        unpadded_data = PKCS7Padding.unpad(decrypted_data)
        return unpadded_data

class OFBMode(CipherMode):
    def __init__(self, cipher : NewBlockCipher, iv):
        super().__init__(cipher)
        if len(iv) != self.cipher.block_size:
            raise ValueError(f"IV harus berukuran {self.cipher.block_size} bytes.")
        self.iv = iv

    def encrypt(self, plaintext):
        padded_plaintext = PKCS7Padding.pad(plaintext, self.cipher.block_size)
        ciphertext = b''
        feedback = self.iv

        for i in range(0, len(padded_plaintext), self.cipher.block_size):
            # Enkripsi feedback
            encrypted_feedback = self.cipher.encrypt_block_bytes(feedback)
            block = padded_plaintext[i:i + self.cipher.block_size]
            # XOR dengan blok plaintext
            encrypted_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
            ciphertext += encrypted_block
            feedback = encrypted_feedback  # Update feedback dengan hasil enkripsi feedback

        return ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) % self.cipher.block_size != 0:
            raise ValueError("Panjang ciphertext harus kelipatan dari ukuran blok.")

        decrypted_data = b''
        feedback = self.iv

        for i in range(0, len(ciphertext), self.cipher.block_size):
            # Enkripsi feedback
            encrypted_feedback = self.cipher.encrypt_block_bytes(feedback)
            block = ciphertext[i:i + self.cipher.block_size]
            # XOR dengan blok ciphertext
            original_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
            decrypted_data += original_block
            feedback = encrypted_feedback  # Update feedback dengan hasil enkripsi feedback

        unpadded_data = PKCS7Padding.unpad(decrypted_data)
        return unpadded_data

class CTRMode(CipherMode):
    def __init__(self, cipher : NewBlockCipher, nonce):
        super().__init__(cipher)
        if len(nonce) != self.cipher.block_size // 2:
            raise ValueError(f"Nonce harus berukuran {self.cipher.block_size // 2} bytes.")
        self.nonce = nonce
        self.counter = 0

    def get_counter_block(self):
        # Membuat blok counter dengan menggabungkan nonce dan counter
        counter_bytes = self.counter.to_bytes(self.cipher.block_size // 2, 'big')
        return self.nonce + counter_bytes

    def encrypt(self, plaintext):
        padded_plaintext = PKCS7Padding.pad(plaintext, self.cipher.block_size)
        ciphertext = b''

        for i in range(0, len(padded_plaintext), self.cipher.block_size):
            block = padded_plaintext[i:i + self.cipher.block_size]
            counter_block = self.get_counter_block()
            encrypted_counter = self.cipher.encrypt_block_bytes(counter_block)
            encrypted_block = bytes(a ^ b for a, b in zip(block, encrypted_counter))
            ciphertext += encrypted_block
            self.counter += 1  # Increment counter untuk blok berikutnya

        return ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) % self.cipher.block_size != 0:
            raise ValueError("Panjang ciphertext harus kelipatan dari ukuran blok.")

        decrypted_data = b''

        for i in range(0, len(ciphertext), self.cipher.block_size):
            block = ciphertext[i:i + self.cipher.block_size]
            counter_block = self.get_counter_block()
            encrypted_counter = self.cipher.encrypt_block_bytes(counter_block)
            original_block = bytes(a ^ b for a, b in zip(block, encrypted_counter))
            decrypted_data += original_block
            self.counter += 1  # Increment counter untuk blok berikutnya

        unpadded_data = PKCS7Padding.unpad(decrypted_data)
        return unpadded_data