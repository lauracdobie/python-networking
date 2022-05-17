import socket

# create the server
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(("0.0.0.0", 20001))
print("Server up")

while True:
    data, client_address = udp_server.recvfrom(1024)
    print(data)
