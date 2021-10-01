#!/usr/bin/env python3
# check_service_and_sendmail.py
"""
.SYNOPSIS
check_service_and_sendmail.py chequea si los servicios definidos están activos y en caso de no estar corriendo
envia un correo a una lista de destinatarios.

.DESCRIPTION
check_service_and_sendmail.py chequea si los servicios definidos están activos y en caso de no estar corriendo
envia un correo a una lista de destinatarios. Para ello lee un fichero CSV, el usuario y la contraseña 
del remitente se gestionan con variables de entorno en el fichero "~/.bashrc". El script se agrega a "crontab"
para que se ejecute como una tarea programada.

CSV Example(sin espacio entre comas, ubicar en /home/usuario):
nombre,receiver_email
Empleado_1,usuario1@gmail.com
Empleado_2,usuario2@gmail.com

# ~/.bashrc: executed by bash(1) for non-login shells.
EMAIL_USER="remitente@gmail.com"
EMAIL_PASSWD="password"

.EXAMPLE
python check_service_and_sendmail.py

.NOTES
Es necesario instalar el Módulo "PySocks" si vamos enviar el email de alerta detrás de un proxy:
python3 -m pip install pysocks
python3 -m pip install --proxy=http://10.20.30.40:8080 pysocks (Detrás de proxy)

Si vamos a usar una cuenta "gmail", una vez creada deberemos habilitar la opción:
“Allow less secure apps”, https://myaccount.google.com/lesssecureapps

Debemos comprobar que la secuencia de fin de linea del script sea LF y no CRLF (Linux-Windows). Posteriormente,
dar permisos de ejecución y agregar la tarea a "crontab". Por ejemplo, para ejecutar cada 3 minutos el script:

crontab -e
*/3 * * * *     /home/usuario/check_service_and_sendmail.py
"""

import csv, smtplib, ssl, os, subprocess, socket
import socks

def send_mail(service, hostname):
    ##### USAMOS LOS METODOS DEL MÓDULO SOCKS ###############################
    socks.setdefaultproxy(socks.HTTP, '10.40.56.3', 8080)   #socks.setdefaultproxy(TYPE, ADDR, PORT).
    socks.wrapmodule(smtplib)   # Encapsulamos el módulo que pasará a través del Proxy, en este caso "smtplib".
    ##### DECLARAMOS LAS VARIABLES NECESARIAS PARA EL EMAIL #################
    port = 465  # Puerto para SSL, se puede omitir.
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ.get('EMAIL_USER') # Importamos las variables de entorno creadas en ".bashrc".
    password = os.environ.get('EMAIL_PASSWD')
    context = ssl.create_default_context()  # Retorna un nuevo contexto con ajustes por defecto seguros.
    ##### CUERPO DEL EMAIL Y CONTENIDO ######################################
    message = """Subject: "{service}" caido en "{hostname}"

    Alerta "{nombre}", el servicio "{service}" en el servidor "{hostname}" esta caido."""
    ##### LECTURA DEL FICHERO CSV DE DESTINATARIOS Y ENVIO DEL EMAIL ########
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:    # Instanciamos el objeto "server" con la sentencia "with", cerrará la conexión al terminar.
        server.login(sender_email, password)    # Realizamos la conexión al servidor con método "login".
        with open("contacts_file.csv") as file:     # Instanciamos el objeto "file" con la sentencia "with", cerrará el fichero de contactos al terminar.
            reader = csv.reader(file)       # Creamos el objeto "reader" con el método "reader" del módulo "csv" y leemos el contenido del fichero de contactos.
            next(reader)                    # Nos saltamos la lectura del encabezado o primera fila del fichero "csv" de contactos.
            for nombre, receiver_email in reader:   # Leemos todos los campos del fichero de contactos "csv" recorriendo todas las filas.
                server.sendmail(        # Enviamos el email con el método "sendmail" (remitente, destinatarios y formatea el cuerpo del correo "message").
                    sender_email,
                    receiver_email,
                    message.format(nombre=nombre,service=service,hostname=hostname),
                )


if __name__ == '__main__':

    os.system('clear')                  # Limpiamos pantalla de consola.
    hostname = socket.gethostname()     # Obtenemos el nombre del equipo.
    services = ['apache2', 'ssh', 'cups']       # Definimos el array con los servicios.

    for service in services:
        check_service = subprocess.run(['systemctl', 'is-active', service], capture_output=True)    # Usamos la función "run" con el parametro "capture_output". 
        if check_service.returncode == 0:   # Usamos la propiedad "returncode", un valor distinto de 0 es error.
            pass
        else:
            send_mail(service, hostname)