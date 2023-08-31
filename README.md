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

### Testes:
- Para testar o envio/recebimento de arquivos, troque `FILENAME` e `FILETYPE` no client e no server.
- Além disso, lembre-se de iniciar o server antes do client.
