import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8081))
server_socket.listen()
print("Waiting for connection")
connection_socket, address = server_socket.accept()
print("Client connected")

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

message = "Hello, thanks for connecting \nHere is another message"
send_text(connection_socket, message)

client_message = next(get_text(connection_socket))
print(client_message)

connection_socket.close()
server_socket.close()

