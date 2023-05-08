import socket

#localizacao do servidor
HOST = '127.0.0.1'
PORT = 10000

'''
Cria socket e conecta com o servidor

Entrada: 

Saida: socket
'''
def iniciaConexao():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    return sock

'''
Inicializa e implementa loop principal do cliente
'''
def main():

    sock = iniciaConexao()

    print('Digite "ajuda" para obter instrucoes')

    while True:

        requisicao = input('-- ')

        match requisicao:

            case 'Operacoes':

                print('As operacoes permitidas sao: consulta e insercao')
                print('Para realizar a consulta, digite "consulta"')
                print('Para realizar a insercao, digite "inserir"')

            case 'Fim':

                print('A conexão foi encerrada')
                sock.send('fim'.encode())
                sock.close()
                return

            case 'ajuda':

                print('Digite "Operacoes" para exibir as operacoes')
                print('Digite "Fim" para encerrar a conexao')

            case _:

                requisicao = requisicao.strip() + '\n'
                sock.send(requisicao.encode())
                resposta = sock.recv(1024)
                print(str(resposta, encoding='utf-8'))

main()