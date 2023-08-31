from socket import *
from rdt_server import *

FILENAME = '../assets/pato'       # Nome do arquivo a ser enviado
RESPONSE = 'response-client'   # Nome do arquivo a ser recebido
FILETYPE = 'jpg'        # Tipo do arquivo a ser enviado/recebido

RDT = RDT_SERVER()

file = open(RESPONSE + '.' + FILETYPE, 'wb')

while True:
    data = RDT.receive()
    if not data: break
    file.write(data)

file.close()

file = open(FILENAME + '.' + FILETYPE, 'rb')

while True:
    data = file.read(RDT.BUFFERSIZE - RDT.HEARDERSIZE)
    RDT.send_pkg(data)
    if not data: break

file.close()

RDT.close_connection()
