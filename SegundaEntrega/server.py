from socket import *
from rdt_server import *

RDT = RDT_SERVER()

file = open("recebidoClient.jpg",'wb')

while True:
    data = RDT.receive()
    if not data: break
    file.write(data)

file.close()

file = open("./Assets/pato.jpg", "rb")

while True:
    data = file.read(RDT.BUFFERSIZE-800)
    RDT.send_pkg(data)
    if not data: break

file.close()

RDT.close_connection()






