import os
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding


class my_class_threading:
    def __init__(self, path_file, key):
        self.path_file = path_file
        self.decryption_key = key

    def AES_CBC_128(self):
        file_data = b""
        with open(self.path_file, 'rb') as encrypted_file:
            while True:
                data = encrypted_file.read(30720)
                if not data:
                    break
                else:
                    file_data += data

        iv = file_data[-16:]
        cipher = AES.new(self.decryption_key, AES.MODE_CBC, iv)
        normal_data = cipher.decrypt(file_data[22: -16:])
        unpadding_data = Padding.unpad(normal_data, 16)
        with open(self.path_file[:-7], 'wb') as normal_file:
            normal_file.write(unpadding_data)
        del file_data
        os.remove(self.path_file)

    def AES_CBC_256(self):
        file_data = b""
        with open(self.path_file, 'rb') as encrypted_file:
            while True:
                data = encrypted_file.read(30720)
                if not data:
                    break
                else:
                    file_data += data

        iv = file_data[-16:]
        cipher = AES.new(self.decryption_key, AES.MODE_CBC, iv)
        normal_data = cipher.decrypt(file_data[22: -16:])
        unpadding_data = Padding.unpad(normal_data, 16)
        with open(self.path_file[:-7], 'wb') as normal_file:
            normal_file.write(unpadding_data)
        del file_data
        os.remove(self.path_file)

    def AES_GCM_256(self):
        file_data = b''
        with open(self.path_file, 'rb') as encrypted_file:
            while True:
                data = encrypted_file.read(30720)
                if not data:
                    break
                else:
                    file_data += data

        iv = file_data[-16:]
        cipher = AES.new(self.decryption_key, AES.MODE_GCM, iv)
        normal_data = cipher.decrypt(file_data[22: -16:])
        unpadding_data = Padding.unpad(normal_data, 16)
        with open(self.path_file[:-7], 'wb') as normal_file:
            normal_file.write(unpadding_data)
        del file_data
        os.remove(self.path_file)
