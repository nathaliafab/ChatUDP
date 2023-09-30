import socket
import threading
import random

class RDT_Client:
    def __init__(self):
        self.BUFFER_SIZE = 1024
        self.num_seq = b'0'
        self.expected_num_seq = b'1'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.SERVER = ('localhost', 9999)
        self.correct_ACK = True
        self.client.bind(('localhost', random.randint(8000, 9000)))

    def send_pkt(self, msg):
        self.num_seq = b'0' if (self.num_seq == b'1') else b'1'
        pkt = self.num_seq + msg
        self.client.sendto(pkt, self.SERVER)
        self.correct_ACK = False
        while not self.correct_ACK:
            if socket.timeout:
                break

    def start(self):
        name = input('Digite seu nome: ')
        self.send_pkt(f'hi, meu nome eh:{name}'.encode())
        t = threading.Thread(target=self.receive_message)
        t.start()
        while True:
            message = input()
            self.send_pkt(f'{name}: {message}'.encode())
            if message == 'bye':
                t.join()
                break

    def receive_message(self):
        while True:
            try:
                message, _ = self.client.recvfrom(self.BUFFER_SIZE)
                if (message == b'0' or message == b'1'):
                    self.correct_ACK = True
                else:
                    print(message.decode())
            except:
                pass
