from socket import *
import threading

def handle_client(client_socket, client_address, other_client_socket):
    # Loop to receive messages from the client
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break
        # Print the received message and forward it to the other client
        print(f'{client_address}: {data.decode()}')
        other_client_socket.send(data)
    
    # Close the client socket when communication is complete
    print(f'Closing connection with {client_address}')
    client_socket.close()

def start_chat_server():
    # Create a TCP socket and bind it to a port
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('localhost', 12000))
    server_socket.listen()

    # Start the main server loop
    while True:
        # Wait for two clients to connect
        print('Waiting for two clients to connect...')
        client1_socket, client1_address = server_socket.accept()
        print(f'Client 1 connected: {client1_address}')
        client2_socket, client2_address = server_socket.accept()
        print(f'Client 2 connected: {client2_address}')

        # Start two threads to handle the chat between the clients
        client1_thread = threading.Thread(target=handle_client, args=(client1_socket, client1_address, client2_socket))
        client1_thread.start()
        client2_thread = threading.Thread(target=handle_client, args=(client2_socket, client2_address, client1_socket))
        client2_thread.start()

def receive_messages(client_socket):
    while True:
        # Receive data from the server
        data = client_socket.recv(1024)
        if not data:
            break
        # Print the received message
        print("Them: ", data.decode())


def start_chat_client():
    # Create a TCP socket and connect to the server
    server_address = input("Input the server IP or hostname: ")
    if (server_address == "1"): server_address = "localhost"
    server_port = 12000
    client_socket = socket(AF_INET, SOCK_STREAM)
    print(server_address)
    client_socket.connect((server_address, server_port))
    print(f'Connected to server at {server_address}:{server_port}')

    # Loop to send messages to the server

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    print("Type 'Quit' to leave")
    # Loop to send messages
    while True:
        # Send a message to the server
        message = input()
        if (message == "Quit"):break
        else: client_socket.send(message.encode())

    # Close the client socket when communication is complete
    #client_socket.close()

# Prompt the user to choose between server and client mode
mode = input('Select mode (s for server, c for client): ')

if mode == 's':
    # Start the chat server
    start_chat_server()
elif mode == 'c':
    # Start the chat client
    start_chat_client()
else:
    print('Invalid mode selected')