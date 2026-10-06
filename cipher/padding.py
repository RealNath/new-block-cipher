class PKCS7Padding:
    @staticmethod
    def pad(value, block_size):
        # Memasukkan padding ke dalam input value agar panjangnya menjadi kelipatan dari block_size.
        # Padding scheme yang digunakan adalah PKCS#7.
        padding_length = block_size - (len(value) % block_size)
        padding = bytes([padding_length] * padding_length)
        return value + padding

    @staticmethod
    def unpad(value):
        # Menghapus padding dari input value yang telah dipad.
        # Padding scheme yang digunakan adalah PKCS#7.
        if not value:
            raise ValueError("Nilai input tidak boleh kosong.")

        padding_length = value[-1]

        if padding_length < 1 or padding_length > len(value):
            raise ValueError("Panjang padding tidak valid.")

        if value[-padding_length:] != bytes([padding_length] * padding_length):
            raise ValueError("Bytes padding tidak valid.")

        return value[:-padding_length]