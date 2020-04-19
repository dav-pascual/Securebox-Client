#!/usr/bin/python3
"""Modulo que se encarga de la gestion de clientes
"""

import requests
import config
import os
import sys
from cipher import gen_id
from Crypto.PublicKey import RSA


def create_id(nombre, email):
    """Crea una nueva identidad en el sistema con el nombre e email especificados.
       Creará un par nuevo de claves publica/privada si es necesario.
       IN:
            - nombre: nombre con el cual nos queremos registrar
            - email: email con el cual nos queremos registrar
    """
    url = config.API_URL + config.ENDPOINT['register_id']
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
        print("\n-> Error al registrar identidad:\n"
              "\t- Codigo: {}\n\t- Info: {}".format(r.json()['http_error_code'], r.json()['description']))
        sys.exit()
    else:
        print("-> Identidad con ID#{} creada correctamente".format(r.json()['userID']))


def get_public_key(user_id):
    """Devuelve la clave publica de un usuario dado su user Id (NIA).
       IN:
            - user_id: ID del usuario que queremos obtener su clave publica
    """
    # LLamada al API Rest
    url = config.API_URL + config.ENDPOINT['publicKey']
    args = {'userID': user_id}
    headers = {"Authorization": "Bearer " + config.TOKEN}
    r = requests.post(url, json=args, headers=headers)
    if not r.ok:
        print("\n-> Error al obtener la clave publica de ID {}:\n"
              "\t- Codigo: {}\n\t- Info: {}".format(user_id, r.json()['http_error_code'], r.json()['description']))
        sys.exit()
    else:
        print("-> Recuperando clave pública de ID {}...OK".format(user_id))
        pk = r.json()['publicKey']
        if pk is None:
            print("-> Error: El usuario con ID {} no esta registrado en el sistema.".format(user_id))
            sys.exit()
        else:
            return pk


def search_id(datasearch):
    """Busca y muestra los usuarios con el nombre o email especificado en datasearch
       IN:
            - datasearch: contenido que queremos buscar
    """
    url = config.API_URL + config.ENDPOINT['search_id']
    # LLamada al API Rest
    headers = {"Authorization": "Bearer " + config.TOKEN}
    args = {'data_search': datasearch}
    r = requests.post(url, json=args, headers=headers)
    if not r.ok:
        print("\n-> Error al buscar usuario\n"
              "\t- Codigo: {}\n\t- Info: {}".format(r.json()['http_error_code'], r.json()['description']))
        sys.exit()
    else:
        users = r.json()
        if len(users) > 0:
            print("{} usuarios encontrados:".format(len(users)))
            for index, user in enumerate(users):
                print("[{}] {}, {}, ID: {}".format(index+1, user['nombre'], user['email'], user['userID']))
        else:
            print("No se han encontrado usuarios con el nombre o email especificado.")


def delete_id(user_id):
    """Borra una identidad existente en el sistema. Solo podra ser borrada por el usuario que la creo
       IN:
            - user_id: id del usuario que queremos eliminar del SecureBox
    """
    url = config.API_URL + config.ENDPOINT['delete_id']
    # LLamada al API Rest
    headers = {"Authorization": "Bearer " + config.TOKEN}
    args = {'userID': user_id}
    r = requests.post(url, json=args, headers=headers)
    if not r.ok:
        print("\n-> Error al borrar identidad:\n"
              "\t- Codigo: {}\n\t- Info: {}".format(r.json()['http_error_code'], r.json()['description']))
        sys.exit()
    else:
        print("-> Solicitando borrado de la identidad #{}...OK".format(r.json()['userID']))
        print("-> Identidad con ID#{} borrada correctamente".format(r.json()['userID']))
