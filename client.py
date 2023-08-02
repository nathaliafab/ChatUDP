from socket import *

HOST = 'localhost'      # Endereco IP do Servidor
PORT = 5000             # Porta que o servidor está
BUFFER_SIZE = 1024      # Tamanho do buffer
FILENAME = 'pato'       # Nome do arquivo a ser enviado
RESPONSE = 'response'   # Nome do arquivo a ser recebido
FILETYPE = 'jpg'        # Tipo do arquivo a ser enviado/recebido
DEST = (HOST, PORT)     # Destino da mensagem
UDP = socket(AF_INET, SOCK_DGRAM) # Cria o socket UDP

f = open(FILENAME + '.' + FILETYPE, 'rb')

print('Enviando...\n')

UDP.sendto("Enviando!".encode(), DEST) # Envia uma mensagem para o servidor

while True:
    data = f.read(BUFFER_SIZE) # Lê os dados do arquivo
    #print(data)
    UDP.sendto (data, DEST)  # Envia os dados lidos para o servidor
    if not data: break # Se não tiver mais dados para enviar, sai do loop

print('Enviado!\n')
f.close()

print('Esperando resposta...\n')

data, server = UDP.recvfrom(BUFFER_SIZE) # Recebe a mensagem do servidor

print('Recebendo...\n')

f = open(RESPONSE + '.' + FILETYPE, 'wb') # Abre o arquivo para escrita

while True:
    data, server = UDP.recvfrom(BUFFER_SIZE)
    f.write(data)
    #print(data)
    if not data: break
    
print('Recebido!\n')
f.close()

UDP.close()