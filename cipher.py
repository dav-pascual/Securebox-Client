#!/usr/bin/python3
# Modulo de cifrado, firma de archivos y generacion de claves
import os
import config
import sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


def gen_id():
    """Genera un nuevo par de claves publica/privada si no existen
    """
    filepath_priv = os.path.abspath(os.path.join(config.KEYS_DIR, 'private.pem'))
    filepath_publ = os.path.abspath(os.path.join(config.KEYS_DIR, 'public.pem'))

    if not os.path.isfile(filepath_priv) or not os.path.isfile(filepath_publ):
        key = RSA.generate(2048)
        private_key = key.export_key()
        with open(filepath_priv, "wb") as file_out:
            file_out.write(private_key)

        public_key = key.publickey().export_key()
        with open(filepath_publ, "wb") as file_out:
            file_out.write(public_key)
        print("-> Generando par de claves RSA de 2048 bits...OK")
    else:
        print("-> Generando par de claves RSA de 2048 bits...Ya existen!")


def sign(fichero):
    """Firma el fichero recibido..
       El fichero a firmar debe estar almacenado en el archivo de config.py
    """
    # Direcciones a usar
    filepath = os.path.abspath(os.path.join(config.FILES_DIR, fichero))
    signed_fp = os.path.abspath(os.path.join(config.FILES_DIR, config.SIGNED_PREFIX + fichero))
    priv_key_path = os.path.abspath(os.path.join(config.KEYS_DIR, 'private.pem'))
    # Obtener clave privada propia
    private_key = RSA.import_key(open(priv_key_path).read())
    # Obtener hash del fichero, cifrarlo con la clave privada y guardar la firma
    if os.path.isfile(filepath):
        with open(filepath, "rb") as f:
            h = SHA256.new(f.read())
            signature = pkcs1_15.new(private_key).sign(h)
            with open(signed_fp, "wb") as signed_file:
                signed_file.write(signature)
                signed_file.write(f.read())
        print("-> Firmando fichero como '{}'...OK".format(config.SIGNED_PREFIX + fichero))
    else:
        print("Error: El fichero especificado no existe")
        sys.exit()


def encrypt(fichero, dest_id):
    """Cifra el fichero recibido.
       El fichero a cifrar debe estar almacenado en el archivo de config.py
    """
    filepath = os.path.abspath(os.path.join(config.FILES_DIR, fichero))
    if os.path.isfile(filepath):
        with open(filepath, "rb") as f:
            data = f.read()
    else:
        print("Error: El fichero especificado no existe")
        sys.exit()

    # Cifrar el archivo con AES
    s_key = get_random_bytes(32)                                  # Clave simetrica aleat 256 bits
    cipher_aes = AES.new(s_key, AES.MODE_CBC)                     # Objeto AES cipher modo CBC e IV aleat 16 bytes
    enc_data = cipher_aes.encrypt(pad(data, AES.block_size))      # Pad y cifrado

    # Cifrar la clave simetrica (sobre digital) con RSA
    from user import get_public_key
    dest_pk = RSA.import_key(get_public_key(dest_id))             # Obtenemos clave publica del receptor
    cipher_rsa = PKCS1_OAEP.new(dest_pk)                          # Objeto RSA cipher
    enc_s_key = cipher_rsa.encrypt(s_key)                         # Cifrado

    # Formateamos el mensaje cifrado final
    encrypted_fp = os.path.abspath(os.path.join(config.FILES_DIR, config.ENC_PREFIX + fichero))
    with open(encrypted_fp, "wb") as encrypted_file:
        encrypted_file.write(cipher_aes.iv)
        encrypted_file.write(enc_s_key)
        encrypted_file.write(enc_data)
    print("-> Cifrando fichero como '{}'...OK".format(config.ENC_PREFIX + fichero))
