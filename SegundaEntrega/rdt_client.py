from socket import *
import random

class RDT_CLIENT:

    def __init__(self, ADDRESSPORT = ("localhost", 5000), BUFFERSIZE = 1024):
        self.SENDER_ADDRES = 0
        self.SEQ_NUMBER = 0
        self.ADDRESSPORT =  ADDRESSPORT
        self.BUFFERSIZE = BUFFERSIZE
        self.HEARDERSIZE = 800
        self.UDP = socket(AF_INET, SOCK_DGRAM)
        print("Client running")
    
    def send(self, data):
        print("Enviando para o servidor")
        self.UDP.sendto(data, self.ADDRESSPORT)

    def pkgLossGenerator(self):
        return random.random() < 0.05

    def send_pkg(self, data):
        data = str({
            'seq': self.SEQ_NUMBER,
            'payload' : data
        }).encode()
        ack = False
        while not ack:
            loss = self.pkgLossGenerator()
            if loss == False:
                self.send(data)
            self.UDP.settimeout(2.0)
            try:
                data, self.SENDER_ADDRES = self.UDP.recvfrom(self.BUFFERSIZE)
            except Exception as e:
                print("ACK não recebido, enviando novamente.")
            else:
                ack = self.rcv_ack(data)
                self.UDP.settimeout(None)

    def receive(self):
        print("Recebendo pacote")
        ack = False
        buffer=""
        while ack == False:
            data, self.SENDER_ADDRES = self.UDP.recvfrom(self.BUFFERSIZE)
            data = self.rcv_pkg(data)
            if data != "":
                buffer = data
                ack = True
            else:
                print("Pacote duplicado!")
        print("Recebido")
        return buffer
    
    def send_ack(self, ack):
        if ack:
            data = data = str({
            'seq': self.SEQ_NUMBER,
            'payload' : "ACK"
        }).encode()
        else:
            data = data = str({
            'seq': self.SEQ_NUMBER,
            'payload' : "NACK"
        }).encode()
        loss = self.pkgLossGenerator()
        if loss == False:
            self.send(data)

    def rcv_pkg(self, data):
        data = eval(data.decode())
        SEQ_NUMBER = data['seq']
        payload = data['payload']
        if SEQ_NUMBER == self.SEQ_NUMBER:
            self.send_ack(1)
            self.SEQ_NUMBER = 1 - self.SEQ_NUMBER
            return payload
        else:
            self.send_ack(0)
            return ""
    

    def rcv_ack(self, data):
        data = eval(data.decode())
        SEQ_NUMBER = data['seq']
        payload = data['payload']
        if SEQ_NUMBER == self.SEQ_NUMBER and payload == "ACK":
            self.SEQ_NUMBER = 1 - self.SEQ_NUMBER
            return True
        else:
            return False

    def close_connection(self):
        print("Encerrando socket cliente")
        self.UDP.close()
