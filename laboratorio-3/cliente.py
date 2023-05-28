import rpyc

def iniciaConexao():
    conn = rpyc.connect('127.0.0.1', 10000)
    print(type(conn.root))
    return conn

def fazRequisicoes(conn):
    
    while True:

        req = input("Digite a operação que deseja realizar: ")
        req = req.upper()

        if req == "CONSULTA":
            
            chave = input("Digite o item que deseja consultar: ")
            valor = conn.root.consulta(chave)
            print(valor)

        elif req == "INSERÇÃO":

            chave = input("Digite o item que deseja adicionar: ")
            valor = input("Digite o significado do item a ser adicionado: ")
            conn.root.insere(chave, valor)

        elif req == "REMOÇÃO":

            chave = input("Digite o item que deseja remover: ")
            conn.root.remove(chave)

        elif req == "FIM":
            print("Conexão encerrada")
            conn.close()
            break

        else:
            print("Operações disponíveis:")
            print("---Consulta---")
            print("---Inserção---")
            print("---Remoção---")
            print("---Fim---")

def main():
    conn = iniciaConexao()
    fazRequisicoes(conn)

if __name__ == '__main__':
    main()

