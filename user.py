#!/usr/bin/python3
# Modulo de gestion de clientes

import requests
import config
import logging
import json
import os
from cipher import gen_id
from Crypto.PublicKey import RSA


def create_id(nombre, email):
    url = config.API_URL + config.ENDPOINT['register']
    # Generamos par de claves si no existen y obtenemos la clave publica a registrar
    gen_id()
    publ_key_path = os.path.abspath(os.path.join(config.KEYS_DIR, 'public.pem'))
    public_key = RSA.import_key(open(publ_key_path).read())

    # LLamada al API Rest
    headers = {"Authorization": "Bearer " + config.TOKEN}
    args = {'nombre': nombre,
            'email': email,
            'publicKey': public_key.export_key()}
    r = requests.post(url, json=args, headers=headers)
    if not r.ok:
        logging.error("\n-> Error al registrar identidad:\n"
                      "\t- Codigo: {}\n\t- Info: {}".format(r.json()['http_error_code'], r.json()['description']))
        exit()
    else:
        logging.info("-> Identidad con ID#{} creada correctamente".format(r.json()['userID']))


def get_public_key(user_id):
    """Devuelve la clave publica de un usuario dado su user Id (NIA).
    """
    logging.info("Obteniendo clave publica de {}...".format(user_id))
    url = config.API_URL + config.ENDPOINT['publicKey']
    args = {'userID': user_id}
    headers = {"Authorization": "Bearer " + config.TOKEN}
    r = requests.post(url, json=args, headers=headers)
    if not r.ok:
        logging.error("\n-> Error al obtener la clave publica:\n"
                      "\t- Codigo: {}\n\t- Info: {}".format(r.json()['http_error_code'], r.json()['description']))
        exit()
    else:
        logging.info("-> Obteniendo clave publica...OK")
        return r.json()['publicKey']