from socket import *

HOST = ''           # Endereco IP do Servidor
PORT = 5000         # Porta que o servidor está
BUFFER_SIZE = 1024  # Tamanho do buffer
ORIG = (HOST, PORT) # Origem da mensagem
FILENAME = 'received'
FILETYPE = 'jpg'
UDP = socket(AF_INET, SOCK_DGRAM)   # Cria o socket UDP

UDP.bind(ORIG)  # Associa a porta ao servidor

print('Esperando mensagem...\n')

data, cliente = UDP.recvfrom(BUFFER_SIZE) # Recebe a mensagem do cliente

print('Recebendo...\n')

f = open(FILENAME+'.'+FILETYPE, 'wb') # Abre o arquivo para escrita

while True:
    data, cliente = UDP.recvfrom(BUFFER_SIZE)
    #print(data)
    f.write(data)
    if not data: break

print('Recebido!\n')
f.close()

print('Enviando resposta...\n')

UDP.sendto("Recebido! Enviando resposta...".encode(), cliente) # Envia uma mensagem para o cliente

f = open(FILENAME+'.'+FILETYPE, 'rb') # Abre o arquivo para leitura

while True:
    data = f.read(BUFFER_SIZE)
    #print(data)
    UDP.sendto(data, cliente)
    if not data: break

print('Enviado!\n')
f.close()

UDP.close()