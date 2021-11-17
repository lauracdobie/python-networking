#UDP client
import socket

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message_to_send = str.encode("Hello, I am Sage.")

udp_client.sendto(message_to_send, ("127.0.0.1", 20001))

message_from_server = udp_client.recvfrom(1024)
print(message_from_server)