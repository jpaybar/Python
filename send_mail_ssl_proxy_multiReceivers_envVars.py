#!/usr/bin/env python3
# send_mail_ssl_proxy_multiReceivers_envVars.py
"""
.SYNOPSIS
Envia un correo con SSL detrás de un proxy HTTP a multiples destinatarios cuyas direcciones
están en un fichero CSV, el usuario y la contraseña del remitente se gestionan con variables
de entorno.

.DESCRIPTION
Envia un correo con SSL detrás de un proxy HTTP a multiples destinatarios cuyas direcciones
están en un fichero CSV, el usuario y la contraseña del remitente se gestionan con variables
de entorno, para ello usa las librerias estandar de Python "csv", "os", "smtplib" y "ssl". 
El envio se realiza desde un equipo situado en una red detrás de un proxy HTTP
por lo que tenemos que instalar con "pip" el módulo "PySocks" y después importar "socks".

.EXAMPLE
python3 send_mail_ssl_proxy_multiReceivers_envVars.py

.NOTES
Si vamos a usar una cuenta "gmail", una vez creada deberemos habilitar la opción:
“Allow less secure apps”, https://myaccount.google.com/lesssecureapps

Es necesario instalar el Módulo "PySocks" para importar "socks":
python3 -m pip install pysocks

Si se está detrás de un proxy:
python3 -m pip install --proxy=http://10.20.30.40:8080 pysocks

Editar el fichero "/home/user/.bash_profile", en caso de no existir crearlo e insertar las lineas:

export EMAIL_USER="usuario@gmail.com"
export EMAIL_PASSWD="password"

CSV Example(sin espacio entre comas):
nombre,receiver_email,numEmpleado
Empleado_1,usuario1@gmail.com,1111
Empleado_2,usuario2@gmail.com,2222

Package       Version
------------- -------
pip           20.0.2
pkg-resources 0.0.0
PySocks       1.7.1
setuptools    44.0.0
"""
##### IMPORTAMOS LOS MÓDULOS NECESARIOS #################################

import csv, smtplib, ssl, os
import socks

##### USAMOS LOS METODOS DEL MODULO SOCKS ###############################

socks.setdefaultproxy(socks.HTTP, '10.20.30.40', 8080)   #socks.setdefaultproxy(TYPE, ADDR, PORT)
socks.wrapmodule(smtplib)   # Encapsulamos el modulo que pasará a través del Proxy, en este caso "smtplib".

##### DECLARAMOS LAS VARIABLES NECESARIAS PARA EL EMAIL #################

port = 465  # Puerto para SSL, se puede omitir
smtp_server = "smtp.gmail.com"
sender_email = os.environ.get('EMAIL_USER') # Importamos las variables de entorno creadas en ".bash_profile"
password = os.environ.get('EMAIL_PASSWD')
context = ssl.create_default_context()  # Retorna un nuevo contexto con ajustes por defecto seguros.

##### CUERPO DEL EMAIL Y CONTENIDO ######################################

message = """Subject: Python Scripting

Hola {nombre}, tu numero de empleado es: {numEmpleado}"""

##### LECTURA DEL FICHERO CSV DE DESTINATARIOS Y ENVIO DEL EMAIL ########

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:    # Instanciamos el objeto "server" con la sentencia "with", cerrará la conexión al terminar.
    server.login(sender_email, password)    # Realizamos la conexión al servidor con método "login".
    with open("contacts_file.csv") as file:     # Instanciamos el objeto "file" con la sentencia "with", cerrará el fichero de contactos al terminar.
        reader = csv.reader(file)       # Creamos el objeto "reader" con el método "reader" del módulo "csv" y leemos el contenido del fichero de contactos.
        next(reader)                    # Nos saltamos la lectura del encabezado o primera fila del fichero "csv" de contactos.
        for nombre, receiver_email, numEmpleado in reader:   # Leemos todos los campos del fichero de contactos "csv" recorriendo todas las filas.
            server.sendmail(        # Enviamos el email con el método "sendmail" (remitente, destinatarios y formatea el cuerpo del correo "message").
                sender_email,
                receiver_email,
                message.format(nombre=nombre,numEmpleado=numEmpleado),
            )



