import socket
import struct

IP = "192.168.137.21"
Port = 49000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	a = struct.pack('i', 12)
	print(struct.unpack_from('B', a, 0))
	sock.sendto(a, ((IP, Port)))