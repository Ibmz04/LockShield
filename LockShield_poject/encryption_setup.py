import os
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding

class my_class_threading:
    def __init__(self, file, key):
        self.path_file = file
        self.encryption_key = key

    def AES_CBC_128(self):
        file_data = b''
        with open(self.path_file, 'rb') as normal_file:
            while True:
                data = normal_file.read(30720)
                if not data:
                    break
                else:
                    file_data += data

        if file_data[:22] == b"lockShield_AES_CBC_128":
            pass
        else:
            iv = os.urandom(16)
            cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv)
            padding_data = Padding.pad(file_data, 16)
            encrypted_data = cipher.encrypt(padding_data)
            with open(self.path_file + ".shield", 'wb') as encrypted_file:
                encrypted_file.write(b"lockShield_AES_CBC_128" + encrypted_data + iv)
            del file_data
            os.remove(self.path_file)


    def AES_CBC_256(self):
        file_data = b''
        with open(self.path_file, 'rb') as normal_file:
            while True:
                data = normal_file.read(30720)
                if not data:
                    break
                else:
                    file_data += data

        if file_data[:22] == b"lockShield_AES_CBC_256":
            pass
        else:
            iv = os.urandom(16)
            cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv)
            padding_data = Padding.pad(file_data, 16)
            encrypted_data = cipher.encrypt(padding_data)
            with open(self.path_file + ".shield", 'wb') as encrypted_file:
                encrypted_file.write(b"lockShield_AES_CBC_256" + encrypted_data + iv)
            del file_data
            os.remove(self.path_file)

    def AES_GCM_256(self):
        file_data = b''
        with open(self.path_file, 'rb') as normal_file:
            while True:
                data = normal_file.read(30720)
                if not data:
                    break
                else:
                    file_data += data
        if file_data[:22] == b"lockShield_AES_GCM_256":
            pass
        else:
            iv = os.urandom(16)
            cipher = AES.new(self.encryption_key, AES.MODE_GCM, iv)
            padding_data = Padding.pad(file_data, 16)
            encrypted_data = cipher.encrypt(padding_data)
            with open(self.path_file + ".shield", 'wb') as encrypted_file:
                encrypted_file.write(b"lockShield_AES_GCM_256" + encrypted_data + iv)
            del file_data
            os.remove(self.path_file)














