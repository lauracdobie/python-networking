import socket

def set_up_server(IP_address, port):
    port_int = int(port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_address, port_int))
    server_socket.listen()

    return server_socket

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
    server_socket = set_up_server("0.0.0.0", 8081)
    print("Waiting for client to connect")
    connection_socket, address = server_socket.accept()
    print("Client connected at " + str(address) + ".")

else:
    ip_address = input("Enter an IP address to connect on > ")
    connection_socket = client_connect(ip_address, 8081)
    name = input("Enter your name > ")
    message = name + " connected to the server."
    send_text(connection_socket, message)

end = False 
     
while end == False:
    print("Waiting for message...")
    message = next(get_text(connection_socket))
    print(message)
    reply = input("Enter your message. Type end to exit. > ")
    if reply.lower() == "end":
        end = True
        break
    send_text(connection_socket, reply)