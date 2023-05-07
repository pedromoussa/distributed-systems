import socket
import select
import sys
import threading
import json

#localizacao do servidor
HOST = ''
PORT = 10000

#lista de I/O de interesse
entradas = [sys.stdin]

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

    entradas.append(sock)

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
def atendeRequesicoes(cliSock, endr):

    while True:

        data = cliSock.recv(1024)

        if not data: 

            print(str(endr) + '-> encerrou')

            lock.acquire()

            del conexoes[cliSock]

            lock.release()

            entradas.remove(cliSock)

            cliSock.close() 

            return

        elif str(data, encoding='utf-8') == 'consulta':

            chave = input('Digite o item que deseja consultar:').lower()

            valor = consultaDicionario(chave)

            print(valor)

        elif str(data, encoding='utf-8') == 'inserir':

            chave = input('Digite o item que deseja adicionar ao dicionario:').lower()

            valor = input('Digite seu significado:').lower()

            insereDicionario(chave, valor)

        elif str(data, encoding='utf-8') == 'remover':

            chave = input('Digite o item que deseja remover:').lower()

            removeDicionario(chave)

        else:

            print(str(data, encoding='utf-8') + ': nao e um comando reconhecido')
            print('Os comandos reconhecidos sao: consulta, inserir e remover')

        cliSock.send(data)

'''
Consulta dicionario em busca do valor de um item

Entrada: chave do item

Saida: valor do item
'''
def consultaDicionario(chave):

    lock.acquire()

    with open('dicionario.json', 'r') as arquivo:

        dicionario = json.load(arquivo)

    lock.release()

    return dicionario.get(chave)

'''
Insere um item no dicionario

Entrada: chave e valor do item

Saida: 
'''
def insereDicionario(chave, valor):

    with open('dicionario.json', 'r+') as arquivo:

        dicionario = json.load(arquivo)
        dicionario[chave] = valor

        arquivo.seek(0)

        json.dump(dicionario, arquivo)

        arquivo.truncate()

        print('Item adicionado com sucesso')

    lock.release()

'''
Remove um item do dicionario

Entrada: chave de um item do dicionario

Saida: 
'''
def removeDicionario(chave):

    with open('dicionario.json', 'r+') as arquivo:

        dicionario = json.load(arquivo)

        if chave in dicionario:

            del dicionario[chave]

            json.dump(dicionario, arquivo)

            print('Item removido com sucesso')

        else: print('A chave {chave} nao existe no dicionario')

    lock.release()

'''
Inicializa e implementa o loop principal do servidor
'''
def main():

    #armazena threads criadas
    clientes = []

    sock = iniciaServidor()

    print('Pronto para receber conexões...')

    while True:

        leitura, escrita, excecao = select.select(entradas, [], [])

        for pronto in leitura:

            if pronto == sock:

                cliSock, endr = aceitaConexao(sock)

                print('Conectado com: ', endr)

                cliente = threading.Thread(target=atendeRequesicoes, args=(cliSock, endr))
                cliente.start()
                clientes.append(cliente)

                cliSock.setblocking(False)

                entradas.append(cliSock)

            elif pronto == sys.stdin:

                cmd = input().lower()

                if cmd == 'fim':
                    
                    #aguarda fim das threads para fechar o servidor
                    for c in clientes:
                        c.join()

                    sock.close()
                    sys.exit()

                elif cmd == 'hist':

                    print(str(conexoes.values()))

                elif cmd == 'remover':

                    chave = input('Chave: ')

                    removeDicionario(chave)

            else:
                
                atendeRequesicoes(pronto, conexoes[pronto])

main()
