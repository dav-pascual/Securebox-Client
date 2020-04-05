#!/usr/bin/python3
# Modulo de cifrado, firma de archivos y generacion de claves
import os
import config
import sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15


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
    """Firma el fichero recibido, guardandolo en un archivo con un prefijo seguido del nombre.
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
    else:
        print("Error: El fichero especificado no existe")
        sys.exit()


def encrypt():
    pass


# - encriptar con clave simetrica aleatoria algoritmo AES
# - hacer sobre digital: encriptar clave simetrica con la clave publica del receptor
# - juntar mensaje cifrado, IV y sobre digital con el orden del enunciado
