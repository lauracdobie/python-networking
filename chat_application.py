import socket

# Ask if the user wants to be a client or a server.
# Ask for a port number.
# Set up a server using this port
# Connect the client
# If the user selected server, set up a loop to get a message from the client and allow the user to enter a reply to send from the server, until the user types end.
# If the user selected client, set up a loop to get a message from the server and allow the user to enter a reply to send from the client, until the user types end.
def set_up_server(IP_address, port):
    port_int = int(port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_address, port_int))
    server_socket.listen()

    return server_socket

def accept_client_connection(server_socket):
    connection_socket, address = server_socket.accept()
    
    return connection_socket

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
    connection_socket = accept_client_connection(server_socket)
    print("A client has connected")
    end = False
    while end == False:
        print("Waiting for client message...")
        send_text(client, "Hello, I'm a client!")
        client_message = next(get_text(connection_socket))
        print(client_message)
        reply = input("Enter your message. Type end to exit. >")
        if reply.lower() == "end":
            end == True
            break
        send_text(connection_socket, reply)
        print("Your message has been sent.")
        server_message = next(get_text(client))
        print("Your message has been received: " + server_message)

    server_socket.close()
    client.close()



if selection.lower() == "client":
    port = input("Enter a port number>")
    server_socket = set_up_server("0.0.0.0", port)
    print("Setting up server...")
    client = client_connect("127.0.0.1", port)
    connection_socket = accept_client_connection(server_socket)
    print("You have connected to the server")
    end = False
    while end == False:
        print("Waiting for server message...")
        send_text(connection_socket, "Hello, I'm a server!")
        server_message = next(get_text(client))
        print(server_message)
        reply = input("Enter your message. Type end to exit. >")
        if reply.lower() == "end":
            end == True
            break
        send_text(client, reply)
        print("Your message has been sent")
        client_message = next(get_text(connection_socket))
        print("Your message to the server has been received: " + client_message)
        

    server_socket.close()
    client.close()

