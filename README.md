# Projeto de Infraestrutura de Comunicações - 2023.1

## Primeira Etapa: Transmissão de arquivos com UDP

Implementação de comunicação UDP utilizando a biblioteca Socket na linguagem Python, com envio e devolução de arquivo (o arquivo deve ser enviado pelo cliente, armazenado no servidor e devolvido ao cliente) em pacotes de até 1024 bytes (buffer_size).

- Não é necessária a implementação de transferência confiável nessa etapa.
- Deve-se implementar o envio e devolução de arquivos, reforçando que o envio de strings não é suficiente. Sugerimos que testem o programa para ao menos dois arquivos, como por exemplo um .txt e uma imagem. Outra dica é alterar o nome do arquivo antes da devolução para demonstrar o funcionamento correto do código.
- Uma mensagem ou um arquivo são ou devem ser considerados a mesma coisa, bits, e devem seguir o mesmo fluxo. O que muda é que arquivos ou mensagens maiores que o buffer_size (lembrando de 1024 bytes) devem ser fragmentados em pacotes e reconstruídos no recebedor. 

## Segunda Etapa: Implementando uma transferência confiável com RDT 3.0

Implementação de transferência confiável, segundo o canal de transmissão confiável rdt3.0, apresentado na disciplina e presente no Kurose, utilizando-se do código resultado da etapa anterior.

- Cada passo executado do algoritmo, em tempo de execução, deve ser printado na linha de comando, de modo a se ter compreensão do que está acontecendo.
- Para teste do algoritmo, deve-se implementar um gerador de perdas de pacotes aleatórios, ocasionando timeout no transmissor para tais pacotes e demonstrando a eficiência do rdt3.0 implementado.
- Não é necessário a implementação do checksum, pois o UDP já realiza essa função (e antes do UDP também há um checksum na camada de enlace).

## Terceira Etapa: Chat de sala única com paradigma cliente-servidor

Implementação de um chat de sala única seguindo o paradigma cliente-servidor com as seguintes especificações:

- **Conectar à sala:** Os clientes podem se conectar à sala digitando o comando `hi, meu nome eh <nome_do_usuario>`.

- **Sair da sala:** Os clientes podem sair da sala digitando o comando `bye`.

- **Exibir lista de usuários do chat:** Os clientes podem verificar a lista de usuários na sala com o comando `list`.

- **Exibir lista de amigos:** Os clientes podem ver a lista de amigos com o comando `mylist`.

- **Adicionar usuário à lista de amigos:** Os clientes podem adicionar um usuário à sua lista de amigos com o comando `addtomylist @<nome_do_usuario>`.

- **Remover usuário da lista de amigos:** Os clientes podem remover um usuário de sua lista de amigos com o comando `rmvfrommylist @<nome_do_usuario>`.

- **Banir usuário da sala:** Os clientes podem banir um usuário da sala com o comando `ban @<nome_do_usuario>`. O servidor iniciará uma contagem de votos para banir o usuário, e se a contagem atingir mais da metade dos clientes conectados, o usuário será banido. Todos os clientes receberão uma mensagem do servidor informando o progresso do ban.

### Formato das Mensagens
Cada mensagem enviada na sala segue o formato:
```
<IP>:<PORTA>/~<nome_usuario>: <mensagem> <hora-data>
```

### Funcionalidades Adicionais
- Quando um usuário se conecta à sala, os outros usuários são notificados da nova presença (ex: "João entrou na sala").

- Mensagens enviadas por qualquer cliente são exibidas para todos os outros clientes.

- Não é permitido que dois usuários com o mesmo nome se conectem à sala.

### Implementação Técnica
- Utiliza-se um socket UDP para comunicação entre o servidor e os clientes.

- A transmissão é confiável, implementada em camada de aplicação seguindo o RDT 3.0, conforme descrito no livro "Redes de Computadores e a Internet" do Kurose.

- Permitir que múltiplos clientes se conectem à sala simultaneamente e interajam de acordo com as funcionalidades especificadas.

### Testes:
- Para testar o envio/recebimento de arquivos, troque `FILENAME` e `FILETYPE` no client e no server.
- Além disso, lembre-se de iniciar o server antes do client.
