from fl_networking_tools import ImageViewer
import socket
import pickle

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(("0.0.0.0", 20001))

viewer = ImageViewer()

def get_pixel_data():
    lost_pixels = 0
    viewer.text = lost_pixels
    pixels_received = 0

    while True:
        data, client_address = udp_server.recvfrom(1024)
        message = pickle.loads(data)
        pos = message[0]
        rgba = message[1]
        width = message[2]
        height = message[3]
        total_pixels = width * height
        viewer.put_pixel(pos, rgba)
        pixels_received += 1

        lost_pixels = total_pixels - pixels_received

        viewer.text = lost_pixels



viewer.start(get_pixel_data)
