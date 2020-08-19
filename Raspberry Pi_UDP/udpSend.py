import serial
import time
from struct import *
import struct
from ctypes import *
import socket
import curses
import sys

ser = serial.Serial('/dev/serial0',
                     57600,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout=3)

UDP_IP = "192.168.1.12"
UDP_Port = 49010

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

a = 0
b = 0

while True:
	with open("/root/KP/datalog.txt", "rb") as f:
		for line in f:
			a+=1
			b+=1
			result = line.split(',')
			# print result
			heading = float(result[0])
			alt = float(result[1])
			ax = float(result[2])
			ay = float(result[3])
			az = float(result[4])
			gx = float(result[5])
			gy = float(result[6])
			gz = float(result[7])
			lat = float(result[8])
			long = float(result[9])
			kecepatan = float(result[10])
			Message = struct.pack('!13d', a, heading, alt, ax, ay, az, gx, gy, gz, lat, long, kecepatan, b)
			print ('send', struct.unpack('!13d', Message))
			datalog = open("/root/KP/datalogMatSend.txt", "a")
			datalog.write(str(struct.unpack('!13d', Message)) + "\n")
 			sock.sendto(Message, (UDP_IP, UDP_Port))
			print(type(Message))
			time.sleep(0.01)
			datalog.close()
#	x = struct.pack('<4sB', b'DATA', 64)
#	print(x)
#	sock.sendto(x, (UDP_IP, UDP_Port))