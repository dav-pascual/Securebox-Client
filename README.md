# practica2


1- Mediante la terminal, se invoca al programa securebox_client.py y mediante parametros se le indica la accion updload (en este caso), la direccion del fichero que se quiere compartir y la id del cliente a quien va dirigido el fichero.
  - Libreria argparse: gestion de parametros

2- Nuestro programa **cifra** y **firma** este fichero y lo transfiere al servidor (usando su API REST), para que este a disposicion del cliente destino (otro cliente)
    
  - Para identificarnos en servidor usamos el token solicitado. Se almacena en local, puede hacerse mediante fichero text, .conf, Pickle, sql, etc. Se incluye en las llamadas a la API
    
  - REST tiene recursos (identificados por una URI) y metodos del recurso (definidos mediante interfaz) por ej post o get.
        - Se pude usar la libraria Resquest de python para hacer peticiones con el formato Rest
        - Ejemplos en la documentacion
    
  - Para cifrar y firmar se usa un esquema hibrido.<br>
        - Algoritmo asimetrico usamos RSA 256 bits<br>
        - Algoritmo simetrico usamos AES<br>
        - Hash usamos SHA256<br>
        - La firma va al principio (antes del mensaje y antes de cifrar)<br>
        - Ademas de una clave simetrica aleatoria para el AES, tambien hay que usar un IV (initial vector), por lo que al final queda Mensaje cifrado + Sobre Digital + IV (el orden viene en el enunciado).<br>
        - Libreria pycriptodime: libreria para cifrado y descifrado<br>
        - Para la firma usamos la funcion PKCS#1 v1.5 (RSA)<br>
        - El IV se añade sin encriptar<br>

  - Si se borra una identidad, su token quedará invalidado, por lo que para crear una identidad nueva habra que solicitar 
    nuevo token


Division general trabajo:
  - Gestion de usuarios<br>
        
  - Cifrado y firma de ficheros
  
  - Subida y descarga de ficheros
        

