# Projeto de Infraestrutura de Comunicações - 2023.1

## Primeira Etapa: Transmissão de arquivos com UDP

Implementação de comunicação UDP utilizando a biblioteca Socket na linguagem Python, com envio e devolução de arquivo (o arquivo deve ser enviado pelo cliente, armazenado no servidor e devolvido ao cliente) em pacotes de até 1024 bytes (buffer_size).

- Não é necessária a implementação de transferência confiável nessa etapa.
- Deve-se implementar o envio e devolução de arquivos, reforçando que o envio de strings não é suficiente. Sugerimos que testem o programa para ao menos dois arquivos, como por exemplo um .txt e uma imagem. Outra dica é alterar o nome do arquivo antes da devolução para demonstrar o funcionamento correto do código.
- Uma mensagem ou um arquivo são ou devem ser considerados a mesma coisa, bits, e devem seguir o mesmo fluxo. O que muda é que arquivos ou mensagens maiores que o buffer_size (lembrando de 1024 bytes) devem ser fragmentados em pacotes e reconstruídos no recebedor. 

### Testes:
- Para testar o envio/recebimento do [`arquivo de texto`](/musica.txt) ou [`arquivo de imagem`](/pato.jpg), troque o `FILENAME` e `FILETYPE` no [`client.py`](/client.py) e o `FILETYPE` no [`server.py`](/server.py)

- Além disso, lembre-se de iniciar o [`server.py`](/server.py) antes do [`client.py`](/client.py)
