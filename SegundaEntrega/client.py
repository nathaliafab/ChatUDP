from socket import *
from rdt_client import *

FILENAME = '../assets/8ab433c58dc0ef160212745bf3973bef'       # Nome do arquivo a ser enviado
RESPONSE = 'response-server'   # Nome do arquivo a ser recebido
FILETYPE = 'jpg'        # Tipo do arquivo a ser enviado/recebido

RDT = RDT_CLIENT()  # Inicializa o cliente

file = open(FILENAME + '.' + FILETYPE, 'rb')    # Abre o arquivo a ser enviado

while True: # Envia o arquivo
    data = file.read(RDT.BUFFERSIZE - RDT.HEARDERSIZE)
    RDT.send_pkg(data)
    if not data: break
file.close()

file = open(RESPONSE + '.' + FILETYPE, 'wb')    # Cria o arquivo a ser recebido

while True: # Recebe o arquivo de resposta
    data = RDT.receive()
    if not data: break
    file.write(data)
file.close()

RDT.close_connection()  # Encerra a conexão
    