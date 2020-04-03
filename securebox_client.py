#!/usr/bin/python3
# Cliente SecureBox

import argparse
import logging
import pdb
import user

# pdb.set_trace() # Para debuguear
logging.basicConfig(level=logging.DEBUG)


def main():
    # Procesado de parametros de entrada
    parser = argparse.ArgumentParser()
    parser.add_argument("--create_id", nargs='+',
                        help="Crea una nueva identidad. Uso: --create_id nombre email")
    parser.add_argument("--search_id",
                        help="Busca un usuario con nombre o correo. Uso: --search_id cadena")
    parser.add_argument("--delete_id",
                        help="Borra la identidad con ID id. Uso: --delete_id id")
    args = parser.parse_args()

    if args.create_id:
        if len(args.create_id) == 2:
            user.create_id(args.create_id[0], args.create_id[1])
        else:
            logging.error('\n-> Error de parametros, uso: --create_id nombre email')
            exit()


if __name__ == '__main__':
    main()
