from socket import *    
import threading 

def receive_messages(client_socket, client_state):
    while client_state[0] == True: 
        data = client_socket.recv(1024)
        if (data.decode() == "Quitting" and  client_state[0] == True):
            client_state[0] = False
            break
        else:
            if data.decode() == "Quitting": pass
            else: print("Them: ", data.decode())

def start_chat_client():
    
    server_address = input("Input the server IP or hostname: ")
    if (server_address == "1"): server_address = "localhost"
    server_port = 12000 
    client_socket = socket(AF_INET, SOCK_STREAM) 
    client_socket.connect((server_address, server_port)) 
    print(f'Connected to server at {server_address}:{server_port}') 
    client_state = [True]

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,client_state))
    receive_thread.start()

    print("Type 'Quit' to leave")

    while client_state[0] == True:
        message = input()
        if (message == "Quit" or client_state[0] == False):
            client_state[0] = False
            break
        
        else: client_socket.sendall(message.encode())

    client_socket.send("Quitting".encode())
    receive_thread.join()

    while True:
        print("Sending Confirmation to Server and waiting confirmation form server")
        client_socket.send("ThreadFinished".encode())
        data = client_socket.recv(1024)
        if (data.decode() == "FinishedServer"): break
    
    client_socket.shutdown(SHUT_WR)
    client_socket.close()

start_chat_client()