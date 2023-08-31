from socket import *
from rdt_client import *

RDT = RDT_CLIENT()

file = open("./Assets/teste.jpg","rb") 

while True:
    data = file.read(RDT.BUFFERSIZE-800)
    RDT.send_pkg(data)
    if not data: break
file.close()

file = open("recebidoServer.jpg",'wb')

while True:
    data = RDT.receive()
    if not data: break
    file.write(data)

file.close()

RDT.close_connection()
    