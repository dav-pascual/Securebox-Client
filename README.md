# SecureBox Client

SecureBox is a service hosted at [UAM-EPS](https://www.uam.es/EPS/Home.htm?language=en) servers, and provides:
- **Identity repository**, in the style of a [PGP key server](https://pgp.mit.edu/). In this repository users can register their identity (public key and identification data), so that other users can search for them, retrieve their public key and send them files.
- **File storage**. The above files are not sent directly to the recipient user, but are stored on the server, so that users can download them later.

The aim of this project is building a client for SecureBox, which interacts with SecureBox over API REST. It will be able to:
- Encrypt and sign files locally.
- Send a file to the SecureBox service, previously encrypted and signed.
- Receive a file stored in SecureBox and check its digital signature after downloading and decrypting.
- Manage identities: Create, export, search and delete users in SecureBox.

## Built with

- Python 3
- [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html), argsparse & request libraries.


## Usage
Consult [wiki](https://github.com/dav-pascual/Securebox-client/wiki/SecureBox-Client#uso-del-programa) or run at the root of the project to obtain more info:
> $ python3 securebox_client.py -h

The user ID and token must be specified in the config.py configuration file.

## Wiki
You can find more detailed info about the design, implementation and use of the program at the [wiki](https://github.com/dav-pascual/Securebox-client/wiki/SecureBox-Client#uso-del-programa) (currently only avaible in spanish).

https://github.com/dav-pascual/Securebox-client/wiki
