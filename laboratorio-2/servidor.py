import socket
#import select
import sys
import threading
import json
import os

#localizacao do servidor
HOST = ''
PORT = 10000

#lista de I/O de interesse
'''
foi removida pois o sys.stdin nao funcionava corretamente no windows
junto ao select, entao optei por utilizar apenas as threads
'''
#entradas = []

#conexoes ativas
conexoes = {}

#lock para acesso de 'conexoes'
lock = threading.Lock()

'''
Cria um socket de servidor e o coloca
em modo de espera por conexoes

Entrada: 

Saida: socket criado
'''
def iniciaServidor():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))

    sock.listen(5)

    sock.setblocking(False)

    return sock

'''
Aceita pedido de conexao de um cliente

Entrada: socket do servidor

Saida: novo socket da conexao e endereco do cliente
'''
def aceitaConexao(sock):

    cliSocket, endr = sock.accept()

    lock.acquire()

    conexoes[cliSocket] = endr

    lock.release()

    return cliSocket, endr

'''
Recebe mensagens e envia as respostas ou confirmacoes ao cliente

Entrada: socket da conexao e endereco do cliente

Saida: 
'''
def atendeRequisicoes(cliSock, endr):

    while True:

        try:

            requisicao = recebeEntrada(cliSock)

            if not requisicao:

                print(str(endr) + '-> encerrou')

                lock.acquire()

                del conexoes[cliSock]

                lock.release()

                cliSock.close()

                if not conexoes:

                    for sock in conexoes.keys():
                        sock.close()

                    print('Não há mais conexões ativas com clientes. Deseja encerrar o servidor? (Y/N)')

                    while True:
                        
                        cli = sys.stdin.readline().strip()

                        match cli:

                            case 'Y':

                                os._exit(0)

                            case 'N':

                                print('Arguardando novas conexoes...')
                                break

                            case _:

                                print('Digite Y para encerrar e N para continuar aguardando') 

                return
            
            elif requisicao == 'consulta':

                cliSock.send('Digite o item que deseja consultar: '.encode())

                chave = recebeEntrada(cliSock).lower()

                valor = consultaDicionario(chave)

                cliSock.send(valor.encode())

            elif requisicao == 'inserir':

                cliSock.send('Digite o item que deseja adicionar ao dicionario: '.encode())

                chave = recebeEntrada(cliSock).lower()

                cliSock.send('Digite seu significado: '.encode())

                valor = recebeEntrada(cliSock).lower()

                resposta = insereDicionario(chave, valor)

                cliSock.send(resposta.encode())

            elif requisicao == 'remover':

                cliSock.send('Digite o item que deseja remover:'.encode())

                chave = recebeEntrada(cliSock).lower()

                resposta = removeDicionario(chave)

                cliSock.send(resposta.encode())

            else:

                cliSock.send('Comando nao reconhecido\nOs comandos reconhecidos sao: consulta, inserir e remover'.encode())

        except BlockingIOError: pass

        except socket.error as err: print('Erro de socket: ', err)

'''
Recebe a entrada digitada pelo usuario para realizar
as operacoes no dicionario

Entrada: socket

Saida: string digitada pelo usuario ou mensagem de erro
'''
def recebeEntrada(sock):

    size = 1024
    entrada = b''

    while True:

        try:

            data = sock.recv(size - len(entrada))

            if not data:

                return None
            
            entrada += data

            if b'\n' in entrada:

                break

        except BlockingIOError:

            pass

        except socket.error as err:

            print('Erro de socket: ', err)

    return entrada.decode().strip()

'''
Consulta dicionario em busca do valor de um item

Entrada: chave do item

Saida: valor do item
'''
def consultaDicionario(chave):

    lock.acquire()

    with open('dicionario.json', 'r') as arquivo:

        if os.stat('dicionario.json').st_size ==0:

            dicionario = {}

        else:

            dicionario = json.load(arquivo)

    lock.release()

    return dicionario.get(chave)

'''
Insere um item no dicionario

Entrada: chave e valor do item

Saida: confirmacao de sucesso da operacao
'''
def insereDicionario(chave, valor):

    lock.acquire()

    with open('dicionario.json', 'r+') as arquivo:

        if os.stat('dicionario.json').st_size ==0:

            dicionario = {}

        else:

            dicionario = json.load(arquivo)

        dicionario[chave] = valor

        arquivo.seek(0)

        json.dump(dicionario, arquivo)

        arquivo.truncate()

        resposta = 'Item adicionado com sucesso'

    lock.release()

    return resposta

'''
Remove um item do dicionario

Entrada: chave de um item do dicionario

Saida: confirmacao de sucesso da operacao
'''
def removeDicionario(chave):

    lock.acquire()

    with open('dicionario.json', 'r+') as arquivo:

        if os.stat('dicionario.json').st_size ==0:

            dicionario = {}

        else:

            dicionario = json.load(arquivo)

        if chave in dicionario:

            del dicionario[chave]

            json.dump(dicionario, arquivo)

            resposta = ('Item removido com sucesso')

        else: resposta = 'A chave {chave} nao existe no dicionario'

    lock.release()

    return resposta

'''
Inicializa e implementa o loop principal do servidor
'''
def main():

    #armazena threads criadas
    clientes = []

    sock = iniciaServidor()

    print('Pronto para receber conexões...')

    while True:
        
        try:

            cliSock, endr = aceitaConexao(sock)
            print('Conectado com: ', endr)
            cliente = threading.Thread(target=atendeRequisicoes, args=(cliSock, endr))
            cliente.start()
            clientes.append(cliente)
            cliSock.setblocking(False)

        except BlockingIOError:

            pass

        except socket.error as err:

            print('Erro de socket: ', err)              

main()
