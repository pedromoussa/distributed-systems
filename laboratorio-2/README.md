# Atividade 1

## Estilo Arquitetural

Arquitetura em Camadas Cliente-Servidor

## Componentes

1. Acesso e Persistência de Dados:

    - Responsável por armazenar o dicionário no disco e pelas operações de leitura e gravação
    - Deve ser capaz de carregar o dicionário do disco e salvar as inserções e remoções dos dados
    - Pode ser implementado usando um banco de dados ou arquivo de texto formatado, como o JSON

2. Processamento das Requisições:

    - Responsável pelas requisições dos clientes
    - Implementa a lógica para as consultas, inserções e remoções
    - Interage com o componente de acesso e persistência de dados para atualizar o dicionário

3. Interface com o Usuário:

    - Responsável por fornecer uma interface para a interação com o dicionário remoto
    - Pode ser implementado como uma CLI
    - Permite que os usuários façam requisições ao servidor para consulta e inserção no dicionário

A comunicação entre os componentes pode ser feita por meio de sockets TCP/IP para a troca de mensagens entre o cliente e o servidor. 

# Atividade 2

## Lado Cliente

- Interface de Usuário: fornece uma interface para interação entre o usuário e o dicionário remoto. 
- Cliente: Estabelece conexão com o servidor e envia as requisições. 

## Lado Servidor

- Servidor: Recebe requisições dos clientes e gerencia a persistência de dados
- Dicionário Remoto: armazenamento do dicionário e fornece operações de consulta, escrita e remoção. Acessado pelo servidor

## Comunicação

- Cliente envia requisição, contendo o tipo de operação e os parâmetros necessários
- Servidor recebe a mensagem, interpreta e realiza as operações correspondentes no dicionário remoto
- Servidor envia mensagem de resposta ao cliente, informando sucesso da operação ou resultados da operação solicitada

