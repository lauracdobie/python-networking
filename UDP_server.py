# UDP Server
import socket

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(("0.0.0.0", 20001))
print("Server up")

data, client_address = udp_server.recvfrom(1024)
message = str.encode("Thanks for connecting")
udp_server.sendto(message, client_address)
print("Client connected")
print(data)