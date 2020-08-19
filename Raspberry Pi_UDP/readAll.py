import serial
import time
from struct import *
import struct
from ctypes import *
import socket
import curses
from multiprocessing import Process
import sys
import select

IP_Receive = "192.168.137.21"
Port_Receive = 49005

IP_Send = "192.168.137.1"
Port_Send = 49000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_Receive, Port_Receive))

while True:
	data, addr = sock.recvfrom(1024)
	packet_size = len(data)
	if packet_size == 77:
		#header = struct.unpack_from('<4s', data, 0)
		#id = struct.unpack_from('i', data, 77)	
		id = struct.unpack_from('B', data, 5)
		#print(id)
		
		val = struct.unpack_from('f', data, 9)
		val = round(val[0], 3)
		#print(header)
		#print(id)
		#print(type(vel))
		print(val)
		#print(data)

		message = struct.pack('<4sBi8f', 'DATA', null, 17, -0.0573, -0.076, 368.21, 368.2, -999, -999, -999, -999)
		sock.sendto(message, (IP_Send, Port_Send))
