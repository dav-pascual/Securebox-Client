#!/usr/bin/python3
"""Configuration file
"""
USER_ID = 'ID_HERE'
TOKEN = 'TOKEN_HERE'
KEYS_DIR = 'keys'
FILES_DIR = 'files'
SIGNED_PREFIX = 'signed_'
ENC_PREFIX = 'enc_'
API_URL = 'https://tfg.eps.uam.es:8080/api'
ENDPOINT = {"publicKey": '/users/getPublicKey',
            "register_id": '/users/register',
            "search_id": '/users/search',
            "delete_id": '/users/delete',
            "upload": '/files/upload',
            "download": '/files/download',
            "list": '/files/list',
            "delete_file": '/files/delete'}
