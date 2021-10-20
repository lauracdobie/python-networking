import socket

# Ask if the user wants to be a client or a server.
# If a server, ask for the IP address and port.
# Set up a server using this IP address and port
# If the user selects client, connect to server as a client
def set_up_server(IP_address, port):
    port_int = int(port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_address, port_int))
    server_socket.listen()
    print("Waiting for connection")
    # connection_socket, address = server_socket.accept()
    # print("Client connected")
    return server_socket

def accept_client_connection(server_socket):
    connection_socket, address = server_socket.accept()
    print("Client connected")

def client_connect(IP_address, port):
    port_int = int(port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP_address, port_int))
    print("Connected")

selection = input("Do you want to be a client or a server?")

if selection.lower() == "server":
    IP_address = input("Enter an IP address >")
    port = input("Enter a port number>")
    server_socket = set_up_server(IP_address, port)
    client_connect("127.0.0.1", 8081)
    accept_client_connection(server_socket)
    message = input("Enter your message")



if selection.lower() == "client":
    server_socket = set_up_server("0.0.0.0", 8081)
    client_connect("127.0.0.1", 8081)
    accept_client_connection(server_socket)
    message = input("Enter your message")
