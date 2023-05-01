from socket import *    #Biblioteca dos sockets
import threading        #Biblioteca dos threads

def handle_client(client_socket, client_address, other_client_socket):  #Função que recebe a data do cliente_x e manda pro cliente_y
    while True:     # Loop que recebe as mensagens dos clientes
        data = client_socket.recv(1024) # Recebe a data enviado pelo cliente_x
        #Checa se o "data" recebido pelo cliente é vazio, se sim isso significa que o cliente desconectou e que podemos fechar o server
        #Não está funcionando direito ainda
        if not data:
            break
        #Printa no terminal do servido a mensagem e manda ela pro cliente_y
        #Detalhe que os "data" enviados são em bytes, então pra pritarr tem q converter para string por meio do "decode()"
        print(f'{client_address}: {data.decode()}')
        other_client_socket.send(data)
    
    #Deveria fechar o socket quando a comunicação terminar, novamente não acho q está funcionando corretamente
    print(f'Closing connection with {client_address}')
    client_socket.close()

def start_chat_server(): #Função do server
    #Cria um socket TCP e o associa a um port
    server_socket = socket(AF_INET, SOCK_STREAM) #Cria um socket TCP (SOCK_STREAM) com comunicação IP/V4 (AF_INET)
    server_socket.bind(('localhost', 12000)) #Acossia o IP do server ao IP da máquina atual (localhost) e ao port 12000
    server_socket.listen() #Começa a ouvir por qualquer pedido de conexão

    #Começa o loop do servidor
    while True:
        #Espera os dois clientes conectarem
        print('Waiting for two clients to connect...')
        client1_socket, client1_address = server_socket.accept() #Quando um cliente_1 conecta o seu socket e IP são salvos nessas variáveis
        print(f'Client 1 connected: {client1_address}')
        client2_socket, client2_address = server_socket.accept() #Quando um cliente_2 conecta o seu socket e IP são salvos nessas variáveis
        print(f'Client 2 connected: {client2_address}')
 
        #Começa duas threads para lidar com o chat dos dois clientes.
        #Isso é necessário pois caso contrário o servidor só poderia lidar com um cliente por vez.
        #Cria um thread que realiza a função "handle_client" com os argumentos o socket to cliente 1, o ip do cliente 1 e o socket do cliente 2
        client1_thread = threading.Thread(target=handle_client, args=(client1_socket, client1_address, client2_socket))
        #Começa o threading
        client1_thread.start()
        #Mesma coisa mas usando como argumentos o socket do cliente 2, o Ip do cliente 2 e o socket do cliente 1
        client2_thread = threading.Thread(target=handle_client, args=(client2_socket, client2_address, client1_socket))
        client2_thread.start()

#Função do cliente que recebe as mensagens. Isso tbm ta rodando num thread pois caso contrário o cliente só receberia mensagem depois de mandar uma mensagem
def receive_messages(client_socket):
    while True:
        #Recebe data do servidor
        data = client_socket.recv(1024)
        #Se o server fecha ele deveria quitar da função
        if not data:
            break
        # Printa no terminal do cliente a mensagem recebida pelo cliente 2
        print("Them: ", data.decode())

#Função que inicia a conexão TCP do cliente com o servidor
def start_chat_client():
    #Pede pra colocar o IP do server, se vc colocar 1 ele coloca o IP da sua máquina
    server_address = input("Input the server IP or hostname: ")
    if (server_address == "1"): server_address = "localhost"
    server_port = 12000 #Inidica a port do servidor
    client_socket = socket(AF_INET, SOCK_STREAM) #Cria um socket TCP com a conexão por meio do protocolo IP/V4
    client_socket.connect((server_address, server_port)) #Conecta ao servidor usando o IP e a port do socket
    print(f'Connected to server at {server_address}:{server_port}') #Printa que conectou

    #Thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    #Quit não funciona direito ainda
    print("Type 'Quit' to leave")
    #Loop para mandar mensagens para o servidor
    while True:
        # Pega o input do usuário
        message = input()
        if (message == "Quit"):break
        #Manda pro server, detalhe que a mensagem tem q ser convertida para bytes, por isso do encode()
        else: client_socket.send(message.encode())

    #Quando o usuário digita "Quit" deveria quitar.
    #O problema parece ser q quando o cliente 1 quita e o cliente 2 não, o servidor tenta enviar mensagens para o cliente 1 mesmo que o socket dele já tenha fechado.
    client_socket.close()

#Promt para iniciar o server ou o cliente
mode = input('Select mode (s for server, c for client): ')

if mode == 's':
    #Começa o server
    start_chat_server()
elif mode == 'c':
    #Começa o cliente
    start_chat_client()
else:
    print('Invalid mode selected')