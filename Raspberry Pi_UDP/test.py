import serial
import time
from struct import *
import struct
from ctypes import *
import socket

ser = serial.Serial('/dev/serial0',
                     57600,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout=3)

UDP_IP = "192.168.137.1"
UDP_Port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

a = 0
b = 0
while True:
	with open("/home/pi/datalog.txt", "rb") as f:
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
			Message = struct.pack('!2d', a, heading)
			print ('send', struct.unpack('!2d', Message))
	 		sock.sendto(Message, (UDP_IP, UDP_Port))
	 		time.sleep(1)