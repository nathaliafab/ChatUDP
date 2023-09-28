import socket
import threading
import random

class RDT_Client:
    def __init__(self):
        self.BUFFER_SIZE = 1024      # tamanho do buffer
        self.num_seq = b'0'          # número de sequencia inicial
        self.expected_num_seq = b'1' # primeiro número de sequencia esperado
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.SERVER = ('localhost', 4000)
        self.correct_ACK = True
        self.client.bind(('localhost', random.randint(8000, 9000)))
        self.name = ""

    def send_pkt(self, msg):
        self.num_seq = b'0' if (self.num_seq == b'1') else b'1'
        pkt = self.num_seq + msg
        print(f"sending msg to {self.SERVER}")
        self.client.sendto(pkt, self.SERVER)                     # enviar o pacote em bytes enquanto tiver
        self.correct_ACK = False
        while not self.correct_ACK:
            if socket.timeout:
                print("timeout")
                break

    def receive_message(self):
        while True:
            try:
                message, _ = self.client.recvfrom(self.BUFFER_SIZE)
                if (message == b'0' or message == b'1'):   # se for ACK
                    self.correct_ACK = True
                else:
                    print(message.decode())
            except:
                pass

    def start(self):
        self.name = input("Digite seu nome: ")

        thread = threading.Thread(target=self.receive_message)
        thread.start()

        self.send_pkt(f'hi, meu nome eh:{self.name}'.encode())

        while True:
            message = input()

            self.send_pkt(f'{self.name}: {message}'.encode())

            if message == 'bye':
                thread.join()
                break
