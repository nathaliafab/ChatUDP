from socket import *
from rdt_client import *

FILENAME = '../assets/8ab433c58dc0ef160212745bf3973bef'       # Nome do arquivo a ser enviado
RESPONSE = 'response-server'   # Nome do arquivo a ser recebido
FILETYPE = 'jpg'        # Tipo do arquivo a ser enviado/recebido

RDT = RDT_CLIENT()

file = open(FILENAME + '.' + FILETYPE, 'rb')

while True:
    data = file.read(RDT.BUFFERSIZE - RDT.HEARDERSIZE)
    RDT.send_pkg(data)
    if not data: break
file.close()

file = open(RESPONSE + '.' + FILETYPE, 'wb')

while True:
    data = RDT.receive()
    if not data: break
    file.write(data)

file.close()

RDT.close_connection()
    