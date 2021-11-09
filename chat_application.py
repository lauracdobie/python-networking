import socket

# Ask if the user wants to be a client or a server.
# If a server, ask for the IP address and port.
# Set up a server using this IP address and port
# If the user selects client, connect to server as a client
# Set up a loop to get a message and allow the user to enter a reply, until the user types end.
def set_up_server(IP_address, port):
    port_int = int(port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_address, port_int))
    server_socket.listen()

    return server_socket

def accept_client_connection(server_socket):
    connection_socket, address = server_socket.accept()

def client_connect(IP_address, port):
    print("Connecting...")
    port_int = int(port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP_address, port_int))
    return client_socket

def send_text(sending_socket, text):
    text = text + "\n"
    data = text.encode()
    sending_socket.send(data)

def get_text(receiving_socket):
    buffer = ""

    socket_open = True
    while socket_open:
        data = receiving_socket.recv(1024)

        if not data:
            socket_open = False

        buffer = buffer + data.decode()
        terminator_pos = buffer.find("\n")

        while terminator_pos > -1:
            message = buffer[:terminator_pos]
            buffer = buffer[terminator_pos + 1:]
            yield message
            terminator_pos = buffer.find("\n")

selection = input("Do you want to be a client or a server?")

if selection.lower() == "server":
    port = input("Enter a port number>")
    server_socket = set_up_server("0.0.0.0", port)
    print("Waiting for client to connect")
    client = client_connect("127.0.0.1", port)
    accept_client_connection(server_socket)
    print("A client has connected")
    message = input("Enter your message >")


if selection.lower() == "client":
    server_socket = set_up_server("0.0.0.0", 8082)
    print("Setting up server...")
    client = client_connect("127.0.0.1", 8082)
    accept_client_connection(server_socket)
    print("You have connected to the server")
    message = input("Enter your message >")

