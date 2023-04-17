import socket

HOST = '127.0.0.1' # maquina onde esta o par passivo
PORTA = 5000       # porta que o par passivo esta escutando

# cria socket
sock = socket.socket()

# conecta-se com o par passivo
sock.connect((HOST, PORTA))

while True:
      
      msgSent = input("msg: ")
      sock.send(msgSent.encode())
      
      # imprime a mensagem recebida
      msgRec = sock.recv(2048)
      print(str(msgRec,  encoding='utf-8'))
      
      if msgRec.decode() == 'fim': break
      
# encerra a conexao
sock.close() 
