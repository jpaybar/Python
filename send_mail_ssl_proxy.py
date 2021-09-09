#!/usr/bin/env python3
# send_mail_ssl_proxy.py
"""
.SYNOPSIS
Envia un correo con SSL detrás de un proxy HTTP

.DESCRIPTION
Envia un correo con SSL detrás de un proxy HTTP, para ello usa las librerias estandar de Python
"smtplib" y "ssl". El envio se realiza desde un equipo situado en una red detrás de un proxy HTTP
por lo que tenemos que instalar con "pip" el módulo "PySocks" y después importar "socks"

.EXAMPLE
python3 send_mail_ssl_proxy.py

.NOTES
Si vamos a usar una cuenta "gmail", una vez creada deberemos habilitar la opcion:
“Allow less secure apps”, https://myaccount.google.com/lesssecureapps

Es necesario instalar el Módulo "PySocks" para importar el modulo "socks":
python3 -m pip install pysocks

Si se esta detrás de un proxy:
python3 -m pip install --proxy=http://10.20.30.40:8080 pysocks

Package       Version
------------- -------
pip           20.0.2
pkg-resources 0.0.0
PySocks       1.7.1
setuptools    44.0.0
"""

import smtplib, ssl
import socks
import getpass

##### USAMOS LOS METODOS DEL MODULO SOCKS #####

socks.setdefaultproxy(socks.HTTP, '10.20.30.40', 8080)   # socks.setdefaultproxy(Tipo de Proxy, Dirección IP, Puerto).
socks.wrapmodule(smtplib)   # Encapsulamos el modulo que pasará a través del Proxy, en este caso "smtplib".

##### DECLARAMOS LAS VARIABLES NECESARIAS PARA EL EMAIL #####

port = 465  # Puerto para SSL, se puede omitir
smtp_server = "smtp.gmail.com"
sender_email = "remitente@gmail.com"  # Dirección del Remitente.
receiver_email = "destinatario@gmail.com"  # Dirección del Destinatario.
password = getpass.getpass("Introduce la contraseña y pulsa enter: ")
#password = input("Introduzca la contraseña y pulse enter: ")
message = """\
Subject: Python Script

Este email fue enviado desde un script de Python."""
context = ssl.create_default_context()  # Retorna un nuevo contexto con ajustes por defecto seguros.

##### INSTANCIAMOS EL OBJETO "server" CON LA SENTENCIA "with" QUE CERRARÁ AUTOMATICAMENTE LA CONEXIÓN
##### SIN TENER QUE USAR "server.quit()" PARA CERRAR LA CONEXIÓN CON EL SERVIDOR. POSTERIORMENTE
##### USAMOS EL MÉTODO "login" y "sendmail". 

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
