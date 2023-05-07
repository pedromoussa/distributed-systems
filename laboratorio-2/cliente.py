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

    while True:

        requisicao = input('-- ')

        print('Digite "ajuda" para obter instrucoes')

        match requisicao:

            case '1':

                print('As operacoes permitidas sao: consulta e insercao')
                print('Para realizar a consulta, digite "consulta"')
                print('Para realizar a insercao, digite "insercao"')

            case '2':

                print('A conexão foi encerrada')
                sock.close()

            case 'ajuda':

                print('Digite 1 para exibir as operacoes')
                print('Digite 2 para encerrar a conexao')

            case _:

                sock.send(requisicao.encode())

main()