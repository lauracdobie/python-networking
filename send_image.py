from PIL import Image
import pickle
import socket
from random import randint

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
image = Image.open("raspberrypi.bmp")

width, height = image.size
print("Image size:")
print(width, height)

pixels_lost = 0

for y in range(height):
    for x in range(width):
        pos = (x, y)
        rgba = image.getpixel(pos)
        message = (pos, rgba, width, height)
        data = pickle.dumps(message)
        if randint(0,9) > 0:
            udp_client.sendto(data, ("127.0.0.1", 20001))
        else:
            pixels_lost += 1

print("Pixels lost:")
print(pixels_lost)