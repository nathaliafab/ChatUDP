import socket
import threading
import queue
import os
import time
import datetime

class RDTServer:
    def __init__(self):
        self.BUFFERSIZE = 1024
        self.messages = queue.Queue()
        self.clients = []         
        self.num_seq_list = []    
        self.expected_num_seq = []
        self.timer = 30           
        self.ban_timer = []       
        self.clients_names = []   
        self.ban_counter = []     
        self.banned_names = []    
        self.vote_checker = False
        self.ban_checker = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('localhost', 4000))
        self.banned_index = 0
        self.in_ban_name = ""
        self.in_ban_index = 0

    def start(self):
      print("-- Server rodando --")
      self.start_threads()

    def start_threads(self):
      t1 = threading.Thread(target=self.receive_message)
      t2 = threading.Thread(target=self.broadcast)
      t1.start()
      t2.start()

    def send_ack(self, num_seq, client_address):
        index = self.clients.index(client_address)
        self.server.sendto(self.expected_num_seq[index], client_address)
        self.update_expected_num_seq(num_seq, index)

    def update_expected_num_seq(self, num_seq, index):
        if num_seq == self.expected_num_seq[index]:
            self.expected_num_seq[index] =  b'0' if (self.expected_num_seq[index] == b'1') else b'1'

    def send_pkt(self, msg, address, index):
      print(address)
      self.update_num_seq_list(index)
      pkt = msg
      self.server.sendto(pkt, address)

    def update_num_seq_list(self, index):
      if (self.num_seq_list[index] == b'1'):
        self.num_seq_list[index] = b'0'
      else:
        self.num_seq_list[index] = b'1'

    def receive_message(self):
      while True:
        try:
          message, address = self.server.recvfrom(self.BUFFERSIZE)
          print("Mensagem recebida...")
          self.process_received_message(message, address)
        except:
         pass

    def process_received_message(self, message, address):
        name = message.decode().split(':')[0]
        if name not in self.banned_names:
            self.messages.put((message, address))

    def broadcast(self):
      while True:
        self.process_messages(self.banned_index)

    def process_messages(self, banned_index):
        while not self.messages.empty():
          date_time = datetime.datetime.now()
          local_time = date_time.strftime("%X")
          message, address = self.messages.get()
          ack = message[0]
          message = message[1:]
          name = message.decode().split(':')[1]
          self.add_new_client(address, name, ack)
          self.process_ban_request(message, address, name, local_time, banned_index)
          self.process_client_messages(message, address, name, local_time, banned_index)

    def add_new_client(self, address, name, ack):
        if address not in self.clients and name not in self.banned_names:
            self.clients.append(address)
            self.clients_names.append(name)
            self.num_seq_list.append(b'0')
            self.expected_num_seq.append(b'1')
            self.ban_timer.append(0)
        if name not in self.banned_names:
            self.send_ack(ack, address)

    def process_ban_request(self, message, address, name, local_time, banned_index):
        try:
            index_sender = self.clients.index(address)
        except:
           print("Erro ao obter indice")
           pass
        ban_checker = False
        vote_checker = False
        if (message.decode().split(':')[1].strip()).startswith('ban @'):
            self.handle_ban_request(message, index_sender, name, self.in_ban_name, self.in_ban_index, ban_checker, vote_checker)

    def handle_ban_request(self, message, index_sender, name, in_ban_name, in_ban_index, ban_checker, vote_checker):
        if time.time() >= (self.ban_timer[index_sender] + self.timer):
            in_ban_name = (message.decode().split(':')[1].strip()).split('@')[1]
        for i in range(len(self.clients)):
            if self.clients_names[i] == in_ban_name and name not in self.ban_counter[i]:
                self.update_ban_counter(i, name, index_sender, in_ban_index, ban_checker, vote_checker)

    def update_ban_counter(self, i, name, index_sender, in_ban_index, ban_checker, vote_checker):
        in_ban_index = i
        self.ban_counter[i].append(name)
        self.ban_timer[index_sender] = time.time()
        if len(self.ban_counter[i]) >= 2 * len(self.clients_names) / 3:
            ban_checker = True
            self.banned_index = i
        vote_checker = True

    def process_client_messages(self, message, address, name, local_time, banned_index):
        for i, client in enumerate(self.clients):
            if message.decode().startswith('hi, meu nome eh:'):
                self.handle_new_client(message, address, name, local_time, i, client)
            else:
                self.handle_existing_client(message, address, name, local_time, i, client, banned_index)

    def handle_new_client(self, message, address, name, local_time, i, client):
        name = message.decode().split(':')[1]
        print(name)
        if (name in self.banned_names):
            self.send_pkt(f'[{local_time}] O user {name} está banido.'.encode(), client, i)
            if self.clients[i] == address:
                self.remove_client(i)
        else:
            if i == 0:
                self.ban_counter.append([])
            self.send_pkt(f'[{local_time}]hi, meu nome eh:{name}'.encode(), client, i)

    def remove_client(self, i):
        print(self.clients)
        print(i)
        self.clients.pop(i)
        self.num_seq_list.pop(i)
        self.expected_num_seq.pop(i)

    def handle_existing_client(self, message, address, name, local_time, i, client, banned_index):
        message_content = message.decode().split(':')[1]
        name_request = message.decode().split(':')[0]
        if name_request in self.banned_names:
            self.send_pkt(f'[{local_time}] Voce está banido, e não pode enviar mensagens.'.encode(), address, 1)
        else:
            self.handle_client_requests(message_content, name_request, local_time, client, address, banned_index)

    def handle_client_requests(self, message_content, name_request, local_time, client, address, banned_index):
        i = self.clients.index(client)
        if message_content == " bye":
            self.send_bye_message(local_time, client, name_request)
        elif message_content == " list":
            self.send_client_list(address, local_time)
        elif (message_content.strip()).startswith(' ban'):  # Check for ban command
            self.process_ban_request(message_content.encode(), address, name_request, local_time, banned_index)
            if self.vote_checker:
                self.send_vote_status(local_time, client, banned_index)
        elif (message_content.strip()).startswith(f'@{self.clients_names[i]}'):
            self.send_direct_message(name_request, message_content, local_time, client)
        elif self.vote_checker:
            self.send_vote_status(local_time, client, banned_index)
        elif self.ban_checker:
            self.send_ban_status(local_time, client, banned_index)
        elif not (message_content.strip()).startswith(f'@'):
            self.send_general_message(message_content, local_time, client, name_request)

        self.update_banned_clients(banned_index)
        print(self.clients_names)

    def send_client_list(self, requester_address, local_time):
        i = self.clients.index(requester_address)
        self.send_pkt(f'[{local_time}] {self.clients_names}'.encode(), requester_address, i)


    def send_direct_message(self, name_request, message_content, local_time, client):
        i = self.clients.index(client)
        self.send_pkt(f'[{local_time}] {name_request}: {message_content}'.encode(), client, i)

    def send_vote_status(self, local_time, client, banned_index):
        i = self.clients.index(client)
        self.send_pkt(f'[{local_time}] {len(self.ban_counter[banned_index])}/{len(self.clients_names)} - ban {self.in_ban_name}'.encode(), client, i)

    def send_ban_status(self, local_time, client, banned_index):
        i = self.clients.index(client)
        self.send_pkt(f'[{local_time}] O usuario {self.clients_names[banned_index]} foi banido!!!'.encode(), client, i)

    def send_general_message(self, message, local_time, client, name):
        i = self.clients.index(client)
        self.send_pkt(f'[{local_time}] {name}: {message}'.encode(), client, i)

    def send_bye_message(self, local_time, client, name):
        i = self.clients.index(client)
        self.send_pkt(f'[{local_time}] {name} saiu da sala.'.encode(), client, i)
        print("1")

    def process_ban_request(self, message, address, name, local_time, banned_index):
        try:
            index_sender = self.clients.index(address)
        except:
         pass

        if (message.decode().split(':')[1].strip()).startswith('ban '):
            in_ban_name = (message.decode().split(':')[1].strip()).split('ban ')[1]
            self.handle_ban_request(message, index_sender, name, in_ban_name, self.in_ban_index)


    def handle_ban_request(self, message, index_sender, name, in_ban_name, in_ban_index):
        if time.time() >= (self.ban_timer[index_sender] + self.timer):
            in_ban_name = (message.decode().split(':')[1].strip()).split('ban ')[1]
            self.ban_timer[index_sender] = time.time()
            if in_ban_name not in self.clients_names:
                print(f"User {in_ban_name} not found")
                return
            user_index = self.clients_names.index(in_ban_name)
            self.ban_counter[user_index] = []

        for i in range(len(self.clients_names)):
            if self.clients_names[i] == in_ban_name and name not in self.ban_counter[i]:
                self.update_ban_counter(i, name, index_sender)

    def update_ban_counter(self, i, name, index_sender):
        self.ban_counter[i].append(name)
        self.ban_timer[index_sender] = time.time()
        if len(self.ban_counter[i]) >= len(self.clients_names) / 2:
            self.ban_checker = True
            self.banned_index = i

    def update_banned_clients(self, banned_index):
        if len(self.ban_counter[banned_index]) >= len(self.clients_names) / 2:
            self.banned_names.append(self.clients_names[banned_index])
            for client in self.clients:
                i = self.clients.index(client)
                self.send_pkt(f'[{datetime.datetime.now().strftime("%X")}] O usuario {self.clients_names[banned_index]} foi banido!!!'.encode(), client, i)
            self.remove_client(banned_index)
            self.banned_index = 0

    def handle_bye_request(self, message, name_request):
        if message == " bye":
          index = self.clients_names.index(name_request)
          self.clients.pop(index)
          self.clients_names.pop(index)
          self.ban_counter.pop(index)
          self.num_seq_list.pop(index)
          self.expected_num_seq.pop(index)
          self.ban_timer.pop(index)



