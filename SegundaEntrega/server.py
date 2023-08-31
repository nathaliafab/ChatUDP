from socket import *
from rdt_server import *

FILENAME = '../assets/pato'       # Nome do arquivo a ser enviado
RESPONSE = 'response-client'   # Nome do arquivo a ser recebido
FILETYPE = 'jpg'        # Tipo do arquivo a ser enviado/recebido

RDT = RDT_SERVER()  # Inicializa o servidor

file = open(RESPONSE + '.' + FILETYPE, 'wb')    # Cria o arquivo a ser recebido

while True: # Recebe o arquivo
    data = RDT.receive()
    if not data: break
    file.write(data)
file.close()

file = open(FILENAME + '.' + FILETYPE, 'rb')    # Abre o arquivo a ser enviado em resposta

while True: # Envia o arquivo de resposta
    data = file.read(RDT.BUFFERSIZE - RDT.HEARDERSIZE)
    RDT.send_pkg(data)
    if not data: break
file.close()

RDT.close_connection()  # Encerra a conexão
