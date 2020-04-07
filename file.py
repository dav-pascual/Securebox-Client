#!/usr/bin/python3
# Modulo de gestion de subida y descarga de ficheros

import requests
import config
import os
import sys
import cipher


def upload(fichero, dest_id):
    """Envia un fichero a un usuario subiendolo al servidor,
       firmandolo y encriptandolo de antemano.
    """
    # Firma y encriptacion del fichero
    cipher.sign(fichero)
    cipher.encrypt(config.SIGNED_PREFIX + fichero, dest_id)

    url = config.API_URL + config.ENDPOINT['upload']
    filepath = os.path.abspath(os.path.join(config.FILES_DIR, config.SIGNED_PREFIX + config.ENC_PREFIX + fichero))

    # LLamada al API Rest
    headers = {"Authorization": "Bearer " + config.TOKEN}
    files = {'ufile': (fichero, open(filepath, "rb"))}
    r = requests.post(url, files=files, headers=headers)
    if not r.ok:
        print("\n-> Error al subir archivo {}\n"
              "\t- Codigo: {}\n\t- Info: {}".format(fichero, r.json()['http_error_code'], r.json()['description']))
        sys.exit()
    else:
        print("-> Subiendo fichero a servidor...OK")
        print("Subida realizada correctamente, ID del fichero: {}".format(r.json()['file_id']))


def download():
    pass


def list_files():
    url = config.API_URL + config.ENDPOINT['list']
    # LLamada al API Rest
    headers = {"Authorization": "Bearer " + config.TOKEN}
    r = requests.post(url, headers=headers)
    if not r.ok:
        print("\n-> Error al listar ficheros\n"
              "\t-> Codigo: {}\n\t- Info: {}".format(r.json()['http_error_code'], r.json()['description']))
        sys.exit()
    else:
        files = r.json()['files_list']
        if r.json()['num_files'] > 0:
            print("{} ficheros encontrados:".format(r.json()['num_files']))
            for index, file in enumerate(files):
                print("[{}] ID del fichero: {}".format(index + 1, file))
        else:
            print("No se han encontrado ficheros para el usuario con este token.")


def delete_file():
    pass
