#!/usr/bin/env python3
# cups_resumePrinterFromPause.py
"""
.SYNOPSIS
cups_resumePrinterFromPause.py conecta con el servidor CUPS y consulta el estado de las impresoras instaladas
si alguna está en estado "pause", cancela los trabajos y vuelve a establecer el estado de la impresora
a inactiva para poder aceptar trabajos nuevamente.

.DESCRIPTION
cups_resumePrinterFromPause.py conecta con el servidor CUPS y consulta el estado de las impresoras instaladas
si alguna está en estado "pause", cancela los trabajos y vuelve a establecer el estado de la impresora
a inactiva para poder aceptar trabajos nuevamente. Es necesario instalar el módulo "Pycups".

.EXAMPLE
python cups_resumePrinterFromPause.py

Si lo quisieramos usar como una tarea programada debemos comprobar que la secuencia de fin de linea del script
sea LF y no CRLF si esta creado en un sistema Windows. Posteriormente dar permisos de ejecución y agregar la 
tarea a "crontab". Por ejemplo, para ejecutar cada 3 minutos el script:

crontab -e
*/3 * * * *     /home/usuario/cups_resumePrinterFromPause.py

.NOTES
### para instalar el módulo pycups ###
sudo apt-get install cups
sudo apt-get install libcups2-dev
sudo apt-get install python3-dev

python3 -m pip install pycups
python3 -m pip install --proxy=http://10.20.30.40:8080 pycups (Detrás de un proxy)
"""

import cups
import os

conn = cups.Connection ()   # Construimos la conexión al servidor CUPS con la clase "Connection". "help(cups.Connection)"
printers = conn.getPrinters () # Diccionario de impresoras indexadas por nombres representando las colas de impresión por atributos. "help(cups.Connection.getPrinters)"
pending_jobs = conn.getJobs(which_jobs='not-completed') # Obtiene un listado de trabajos, en este caso los no completados. "help(cups.Connection.getJobs)"

os.system('clear')

for impresora in printers:      # Obtenemos las impresoras instaladas.

        estado = printers[impresora]['printer-state']   # Se consulta el estado de cada impresora.
                             
        if estado != 5: # Evaluamos el estado de la impresora. "3" inactivo, "4" imprimiendo un trabajo y "5" detenido. https://www.cups.org/doc/cupspm.html
                pass
        else:
                for impresiones_pendientes in pending_jobs:     # Vemos todos los trabajos de impresión pendientes para cada impresora que este en "pause" o estado "5".
                        conn.cancelJob(impresiones_pendientes, purge_job=False)
                        # "purge_job" purga los trabajos activos y completados, eliminando todo el historial y los documentos por imprimir de la cola de impresión.
                conn.enablePrinter(impresora)   # Activamos la impresora para que vuelva a gestionar su cola de impresión. "idle" o estado "3"
                print(f'\nLa impresora {impresora} vuelve a estar activa.\n')


                