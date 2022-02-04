#!/usr/bin/python3
"""SecureBox client
"""

import argparse
import config
import user
import cipher
import file


def main():
    """Main function. Input parameters processing.
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--create_id", nargs=2, metavar=("nombre", "email"),
                        help="Create a new identity.")
    group.add_argument("--search_id", metavar="cadena",
                       help="Search a new user by name or email. Use: --search_id cadena")
    group.add_argument("--delete_id", metavar="id",
                       help="Delete identity by ID.")
    group.add_argument("--upload", metavar="fichero",
                       help="Send user to file specified with option --dest_id.")
    group.add_argument("--list_files", action="store_true",
                       help="List all files belonging to a user.")
    group.add_argument("--download", metavar="id_fichero",
                       help="Retrieve file from the server by ID id_fichero and sender specified with"
                            "option --source_id, verify signature and decrypt.")
    group.add_argument("--delete_file", metavar="id_fichero",
                       help="Delete file from server by ID id_fichero.")
    group.add_argument("--encrypt", metavar="fichero",
                       help="Encrypt file, which a user with ID specified with option --dest_id"
                            "will be able to decrypt")
    group.add_argument("--sign", metavar="fichero", help="Sign a file")
    group.add_argument("--enc_sign", metavar="fichero",
                       help="Encrypt and sign a file, combining last two options,"
                            "specifying destination user with option --dest_id.")
    parser.add_argument("--dest_id", metavar="id",
                        help="File receiver ID.")
    parser.add_argument("--source_id", metavar="id",
                        help="File sender ID")
    args = parser.parse_args()

    if args.create_id:
        user.create_id(args.create_id[0], args.create_id[1])
    elif args.search_id:
        user.search_id(args.search_id)
    elif args.delete_id:
        user.delete_id(args.delete_id)
    elif args.upload:
        if args.dest_id:
            file.upload(args.upload, args.dest_id)
        else:
            parser.print_help()
    elif args.list_files:
        file.list_files()
    elif args.download:
        if args.source_id:
            file.download(args.download, args.source_id)
        else:
            parser.print_help()
    elif args.delete_file:
        file.delete_file(args.delete_file)
    elif args.encrypt:
        if args.dest_id:
            cipher.encrypt(args.encrypt, args.dest_id)
        else:
            parser.print_help()
    elif args.sign:
        cipher.sign(args.sign)
    elif args.enc_sign:
        if args.dest_id:
            cipher.sign(args.enc_sign)
            cipher.encrypt(config.SIGNED_PREFIX + args.enc_sign, args.dest_id)
        else:
            parser.print_help()


if __name__ == '__main__':
    main()
