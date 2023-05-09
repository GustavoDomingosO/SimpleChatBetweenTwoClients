from socket import *    
import threading        

quit_code = '01000110'

def handle_client(client_socket, client_address, other_client_socket):  
    while True:     
        data = client_socket.recv(1024)
        if (data.decode() == quit_code):
            other_client_socket.send(quit_code.encode()) #Manda pro outro cliente q vamos quitar
            break
        else:
            print(f'{client_address}: {data.decode()}')
            other_client_socket.sendall(data)
    print(f'Closing connection with {client_address}')  

def start_chat_server(): 

    server_socket = socket(AF_INET, SOCK_STREAM) 
    server_socket.bind(('localhost', 12000)) 
    server_socket.listen() 

    client1_address = None
    client2_address = None
    print('Waiting for two clients to connect...')
    while True:
        
        if(client1_address == None and client2_address == None):
            client1_socket, client1_address = server_socket.accept() 
            print(f'Client 1 connected: {client1_address}')
            client2_socket, client2_address = server_socket.accept() 
            print(f'Client 2 connected: {client2_address}')
        else: break
       
    client1_thread = threading.Thread(target=handle_client, args=(client1_socket, client1_address, client2_socket))
    client2_thread = threading.Thread(target=handle_client, args=(client2_socket, client2_address, client1_socket))
    client1_thread.start()
    client2_thread.start()
    client1_thread.join()
    client2_thread.join()
    while True:
        print("Waiting for confirmation from the clients")
        data1 = client1_socket.recv(1024)
        data2 = client2_socket.recv(1024)
        if (data1.decode() == "ThreadFinished" and data2.decode() == "ThreadFinished"):
            client1_socket.send("FinishedServer".encode())
            client2_socket.send("FinishedServer".encode())
            break
    client1_socket.shutdown(SHUT_WR)
    client2_socket.shutdown(SHUT_WR)
    client1_socket.close()
    client2_socket.close()

start_chat_server()