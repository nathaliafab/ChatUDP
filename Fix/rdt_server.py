import socket
import threading
import queue
import os
import time
import datetime

class RDT_Server:
    def __init__(self):
        self.messages = queue.Queue()
        self.clients = []          # endereços dos clientes conectados
        self.num_seq_list = []     # número de sequencia inicial
        self.expected_num_seq = [] # primeiro número de sequencia esperado       
        self.timer = 30            # tempo em 30 segundos para poder banir um usuário
        self.ban_timer = []        # ultima  vez que um usuario baniu
        self.clients_names = []    # nome dos usuários conectados
        self.ban_counter = []      # lista de usuários que votaram no banimento de determinado usuário
        self.banned_names = []     # lista de usuários banidos
        self.vote_checker = False
        self.ban_checker = False
        self.BUFFER_SIZE = 1024
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('localhost', 9999))

    # envia ACK correto
    def send_ACK(self, num_seq, client_address):
        index = self.clients.index(client_address)
        self.server.sendto(self.expected_num_seq[index], client_address) # envia o ACK com o número de sequencia esperado
        if num_seq == self.expected_num_seq[index]:                 # se o que foi recebido era o esperado, muda o número esperado
            self.expected_num_seq[index] =  b'0' if (self.expected_num_seq[index] == b'1') else b'1'

    # envia pacote para o destino
    def send_pkt(self, msg, address, index):
        self.num_seq_list[index] = b'0' if (self.num_seq_list[index] == b'1') else b'1'
        pkt = msg
        self.server.sendto(pkt, address)                          # enviar o pacote em bytes enquanto tiver

    # thread que recebe as mensagens e coloca em uma fila
    def receive_message(self):
        while True:
            try:
                message, address = self.server.recvfrom(self.BUFFER_SIZE)
                name = message.decode().split(':')[0]
                if name not in self.banned_names:
                    self.messages.put((message, address))
            except:
                pass

    def broadcast(self):
        banned_index = -1
        while True:
            while not self.messages.empty():
                date_time = datetime.datetime.now()
                local_time = date_time.strftime("%X") # tempo atual em HH:MM:SS
                message, address = self.messages.get()     # pega uma mensagem da fila de mensagens
                ack = message[0]                      # extrai o numero de sequencia da mensagem
                message = message[1:]                 

                name = message.decode().split(':')[0]

                if address not in self.clients and name not in self.banned_names:
                    self.clients.append(address)
                    self.num_seq_list.append(b'0')
                    self.expected_num_seq.append(b'1')
                    self.ban_timer.append(0)
                if name not in self.banned_names:
                    self.send_ACK(ack, address)              # ACK for received message

                in_ban_name = ""
                in_ban_index = 0

                # verifica o index da pessoa que mandou 
                try:
                    index_sender = self.clients.index(address)
                except:
                    pass

                self.ban_checker = False
                self.vote_checker = False

                # mensagem de verificação de ban
                if (message.decode().split(':')[1].strip()).startswith('ban @'):

                    if time.time() >= (self.ban_timer[index_sender] + self.timer):          
                        in_ban_name = (message.decode().split(':')[1].strip()).split('@')[1]

                        for i in range(len(self.clients)):
                            # Verifica se o usuário que está banindo não está na lista de banidos
                            if self.clients_names[i] == in_ban_name and name not in self.ban_counter[i]:

                                in_ban_index = i
                                self.ban_counter[i].append(name)
                                self.ban_timer[index_sender] = time.time()
                                if len(self.ban_counter[i]) >= 2*len(self.clients_names)/3:
                                    self.ban_checker = True
                                    banned_index = i
                                    
                                self.vote_checker = True

                # envio de mensagens para todos os clientes
                for i, client in enumerate(self.clients):
                    # primeira mensagem de um novo cliente
                    if message.decode().startswith('hi, meu nome eh:'):
                        name = message.decode().split(':')[1]
                        
                        # se o cliente estiver na lista de banimentos e tenta enviar uma msg, os outros recebem um aviso
                        if (name in self.banned_names):
                            self.send_pkt(f'[{local_time}] O usuario {name} esta banido, nao pode entrar'.encode(), client, i)
                            if self.clients[i] == address:       # se o usuario que tentou entrar estive banido
                                self.clients.pop(i)
                                self.num_seq_list.pop(i)
                                self.expected_num_seq.pop(i)

                        # se nao tiver, adiciona o cliente nas listas e envia a mensagem aos usuarios
                        else:
                            if i == 0:
                                self.clients_names.append(name)
                                self.ban_counter.append([])
                            self.send_pkt(f'[{local_time}]hi, meu nome eh:{name}'.encode(), client, i)
                    else:
                        message_content = message.decode().split(':')[1]
                        name_request = message.decode().split(':')[0]
                        # se o nome de quem enviou a mensagem estiver na lista de banimento, ele recebe um aviso
                        if name_request in self.banned_names:
                            self.send_pkt(f'[{local_time}] Você esta banido, nao pode enviar mensagens'.encode(), address, 1)
                            break
                        
                        else:
                            # se a mensagem for um bye
                            if message_content == " bye":
                                self.send_pkt(f'[{local_time}] {name_request} saiu do chat! :('.encode(), client, i)

                            # se o a mensagem for um comando de listagem
                            elif message_content == " list":
                                if name_request == self.clients_names[i]:
                                    self.send_pkt(f'[{local_time}] {self.clients_names}'.encode(), client, i)
                            
                            # se a mensagem for uma mensagem privada, envia apenas para o destinatário
                            elif (message_content.strip()).startswith(f'@{self.clients_names[i]}'):
                                self.send_pkt(f'[{local_time}] {name_request}:{message_content}'.encode(), client, i)

                            # envia mensagem se um voto for adicionado
                            if self.vote_checker:
                                self.send_pkt(f'[{local_time}] {len(self.ban_counter[in_ban_index])}/{len(self.clients_names)} - ban {in_ban_name}'.encode(), client, i)
                            
                            # envia mensagem se um jogador for banido
                            if self.ban_checker:
                                self.send_pkt(f'[{local_time}] O usuario {self.clients_names[in_ban_index]} foi banido!!!'.encode(), client, i)
                            
                            # se a mensagem nao for privada, envia para todos
                            if not (message_content.strip()).startswith(f'@'):
                                self.send_pkt(f'[{local_time}] {message.decode()}'.encode(), client, i)

                # retira o usuário da lista caso ele seja banido ou saia do chat
                if len(self.ban_counter[banned_index]) >= 2*len(self.clients_names)/3:
                    self.banned_names.append(self.clients_names[banned_index])
                    self.clients.pop(banned_index)
                    self.clients_names.pop(banned_index)
                    self.ban_counter.pop(banned_index)
                    self.num_seq_list.pop(banned_index)
                    self.expected_num_seq.pop(banned_index)
                    self.ban_timer.pop(banned_index)
                    banned_index = 0

                # retira o usuário da lista caso ele saia do chat
                if message.decode().split(':')[1] == " bye":
                    index = self.clients_names.index(name_request)
                    self.clients.pop(index)
                    self.clients_names.pop(index)
                    self.ban_counter.pop(index)
                    self.num_seq_list.pop(index)
                    self.expected_num_seq.pop(index)
                    self.ban_timer.pop(index)

    def start(self):
        t1 = threading.Thread(target=self.receive_message)
        t2 = threading.Thread(target=self.broadcast)

        t1.start()
        t2.start()
