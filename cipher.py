#!/usr/bin/python3
"""Module that handles encryption, file signing and key generation.
"""
import os
import config
import sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


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
       IN:
            - fichero: nomber del fichero que se desea firmar
    """
    # Direcciones a usar
    filepath = os.path.abspath(os.path.join(config.FILES_DIR, fichero))
    signed_fp = os.path.abspath(os.path.join(config.FILES_DIR, config.SIGNED_PREFIX + fichero))
    priv_key_path = os.path.abspath(os.path.join(config.KEYS_DIR, 'private.pem'))
    # Obtener clave privada propia
    try:
        private_key = RSA.import_key(open(priv_key_path).read())
    except (IOError, OSError) as e:
        print("Error al obtener la clave privada")
        sys.exit()
    # Obtener hash del fichero, cifrarlo con la clave privada y guardar la firma
    if os.path.isfile(filepath):
        with open(filepath, "rb") as f, open(signed_fp, "wb") as signed_file:
            data = f.read()
            h = SHA256.new(data)
            signature = pkcs1_15.new(private_key).sign(h)
            signed_file.write(signature)
            signed_file.write(data)
        print("-> Firmando fichero como '{}'...OK".format(config.SIGNED_PREFIX + fichero))
    else:
        print("Error: El fichero especificado no existe")
        sys.exit()


def encrypt(fichero, dest_id):
    """Cifra el fichero recibido.
       El fichero a cifrar debe estar almacenado en el archivo de config.py
       IN:
            - fichero: nombre del fichero que se desea cifrar
            - dest_id: ID del usuario del cual usaremos su clave publica para cifrar
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


def decrypt_s_key(enc_s_key):
    """Descifra la clave simetrica codificada mediante algoritmo RSA con la clave privada
       IN:
            - enc_s_key: Clave simetrica cifrada, la cual queremos descifrar
       OUT: clave simetrica descifrada
    """
    filepath_priv = os.path.abspath(os.path.join(config.KEYS_DIR, 'private.pem'))
    if os.path.isfile(filepath_priv):
        private_key = RSA.import_key(open(filepath_priv).read())
        cipher_rsa = PKCS1_OAEP.new(private_key)
        s_key = cipher_rsa.decrypt(enc_s_key)
        return s_key
    else:
        print("Error: No se encuentra la clave privada")
        sys.exit()


def decrypt_msg(enc_msg, iv, s_key):
    """Descifra un mensaje codificado mediante el algoritmo AES
       IN:
            - enc_msg: fichero que se desea descifrar
            - iv: vector inicial
            - s_key: clave simetrica de descifrado
       OUT: mensaje descifrado
    """
    try:
        cipher_aes = AES.new(s_key, AES.MODE_CBC, iv)
        msg = unpad(cipher_aes.decrypt(enc_msg), AES.block_size)
        print("-> Descifrando fichero...OK")
        return msg
    except (ValueError, KeyError):
        print("Error: Descifrado de mensaje erroneo")
        sys.exit()


def verify_sign(msg, source_id):
    """Verifica que la firma del emisor sea valida en el mensaje recibido
       IN:
            - msg: mensaje del cual queremos verificar su firma
            - source_id: ID del usuario que firmo el mensaje
       OUT: mensaje sin la firma
    """
    signature = msg[:256]
    payload = msg[256:]
    from user import get_public_key
    src_pk = RSA.import_key(get_public_key(source_id))
    h = SHA256.new(payload)
    try:
        pkcs1_15.new(src_pk).verify(h, signature)
        print("-> Verificando firma...OK")
        return payload
    except (ValueError, TypeError):
        print("Error: La firma del archivo no es valida")
        sys.exit()
