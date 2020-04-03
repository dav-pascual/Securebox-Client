#!/usr/bin/python3
# Modulo de cifrado, firma de archivos y generacion de claves
from Crypto.PublicKey import RSA
import os
import logging
import config


def gen_id():
    """Genera un nuevo par de claves publica/privada si no existen
    """
    filepath_priv = os.path.abspath(os.path.join(config.KEYS_DIR, 'private.pem'))
    filepath_publ = os.path.abspath(os.path.join(config.KEYS_DIR, 'public.pem'))

    if not os.path.isfile(filepath_priv) or not os.path.isfile(filepath_publ):
        key = RSA.generate(2048)
        private_key = key.export_key()
        file_out = open(filepath_priv, "wb")
        file_out.write(private_key)
        file_out.close()

        public_key = key.publickey().export_key()
        file_out = open(filepath_publ, "wb")
        file_out.write(public_key)
        file_out.close()
        logging.info("-> Generando par de claves RSA de 2048 bits...OK")
    else:
        logging.info("-> Generando par de claves RSA de 2048 bits...Ya existen!")
