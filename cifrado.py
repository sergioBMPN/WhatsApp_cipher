from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import sys


class AESCipher:

    def __init__(self, key, file, s_key):
        self.key = key
        self.file = file
        self.bs = 1024
        self.exit_file = file + '.enc'
        self.mode = AES.MODE_EAX
        self.session_key = s_key

    def cifrar(self):

        with open(self.file, 'rb') as in_file:
            data = in_file.readlines()
            #data = [x.strip() for x in data] # dejar el \n del final para saber donde acaba la linea
            aes_tag_txt = list()

            for line in data:
                cipher_aes = AES.new(self.session_key, AES.MODE_EAX)
                ct, t = cipher_aes.encrypt_and_digest(line)
                aes_tag_txt.append((cipher_aes, t, ct))

            return aes_tag_txt

    def descifrar(self):
        exit_file = self.file + '.dec'

        with open(self.exit_file, 'rb') as entrada:
            with open(exit_file, 'wb') as salida:
                iv = entrada.read(AES.block_size)
                decipher = AES.new(self.key.encode("utf8"), self.mode, iv)

                bloque = entrada.read(self.bs)

                while len(bloque) != 0:
                    salida.write(decipher.decrypt(bloque))
                    bloque = entrada.read(self.bs)


class Hash_Cipher:
    def __init__(self, file):
        self.file = file

    def get_hash(self, save_out=False):
        bs = 1024
        my_hash = SHA256.new()

        with open(self.file, 'rb') as entrada:
            temp = entrada.read(bs)
            while len(temp) > 0:
                my_hash.update(temp)
                temp = entrada.read(bs)

        # Guarda el contenido del hash en un fichero de salida con la extensión '.hash'
        if save_out:
            ficheroSalida = self.file + '.hash'
            with open(ficheroSalida, 'w') as salida:
                salida.write(my_hash.hexdigest())

        return my_hash


class RSACipher:
    def __init__(self, file, password, hash):
        self.hash = hash
        self.file = file
        self.password = password
        self.private_key_file = 'clave.bin'
        self.public_key_file = 'clave.pub'
        self.length_key = 2048
        self.key = RSA.generate(self.length_key)
        self.private_key = self.key.exportKey(passphrase=password)
        self.public_key = self.key.publickey().exportKey()

        with open(self.private_key_file, 'wb') as private:
            with open(self.public_key_file, 'wb') as public:
                private.write(self.private_key)
                public.write(self.public_key)

    def cifrar_RSA(self):
        with open(self.file + '.enc', 'wb') as out_file:
            recipient_key = RSA.import_key(open(self.public_key_file).read())
            session_key = get_random_bytes(16)

            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            out_file.write(cipher_rsa.encrypt(session_key))

            aes_cipher = AESCipher(self.password, self.file, session_key)
            aes_tag_txt = aes_cipher.cifrar()

            for line in aes_tag_txt:
                out_file.write(line[0].nonce)
                out_file.write(line[1])
                out_file.write(line[2])

    def descifrar_RSA(self):
        with open(self.file + '.enc', 'rb') as fobj:
            key = RSA.import_key(open(self.private_key_file).read(), passphrase=self.password)

            enc_session_key, nonce, tag, ciphertext = [fobj.read(x)
                                                       for x in (key.size_in_bytes(),
                                                                 16, 16, -1)]

            cipher_rsa = PKCS1_OAEP.new(key)
            session_key = cipher_rsa.decrypt(enc_session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt(ciphertext)  # _and_verify(ciphertext, tag)

        print(data.decode())


# TODO: sacar la funcion descifrar de las clases para poder implementar cliente-servidor (entrega final)

if __name__ == '__main__':
    try:
        fichero= sys.argv[1]
        passwd= sys.argv[2]
        my_hash = Hash_Cipher(fichero)
        hash_file = my_hash.get_hash()

        obj = RSACipher(fichero, passwd, hash_file)
        obj.cifrar_RSA()
        obj.descifrar_RSA()
    except:
        print("error, debe introducir el fichero y la contraseña")

