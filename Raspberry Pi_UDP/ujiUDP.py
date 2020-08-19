import serial
import time
import struct
import socket
from multiprocessing import Process
import sys
import select

ser = serial.Serial('/dev/serial0',
                     38400,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout=1)

IP_Send = "192.168.137.1"
Port_Send = 49000

IP_Receive = "192.168.137.21"
Port_Receive = 49005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_Receive, Port_Receive))
packet_size = 1

while True:
	data, addr = sock.recvfrom(1024)
	packet_size = len(data)
	#print("Byte Length ", packet_size)

	if packet_size == 329:
		header = struct.unpack_from('<4s', data, 0)
		# print(header) # DATA

		if header == (b'DATA',):
			# ID offset = 5
			id_data = struct.unpack_from('B', data, 5)
			# print(id_data) # ID Data = 18 pitch, roll, yaw
			timer = struct.unpack_from('f', data, 17)
			timer = round(timer[0], 3)
			airspeed = struct.unpack_from('f', data, 53)
			airspeed = round(airspeed[0], 3)
			groundspeed = struct.unpack_from('f', data, 57)
			groundspeed = round(groundspeed[0], 3)
			pitch = struct.unpack_from('f', data, 153)
			pitch = round(pitch[0], 3)
			roll = struct.unpack_from('f', data, 157)
			roll = round(roll[0], 2)
			yaw = struct.unpack_from('f', data, 161)
			yaw = round(yaw[0], 3)
			mag = struct.unpack_from('f', data, 165)
			mag = round(mag[0], 3)
			lat = struct.unpack_from('f', data, 225) 
			lat = round(lat[0], 3)
			lon = struct.unpack_from('f', data, 229)
			lon = round(lon[0], 3)
			alt = struct.unpack_from('f', data, 237)
			alt = round(alt[0], 3)
			x = struct.unpack_from('f', data, 261)
			x = round(x[0], 3)
			y = struct.unpack_from('f', data, 265)
			y = round(y[0], 3)
			vx = struct.unpack_from('f', data, 273)
			vx = round(vx[0], 3)
			vy = struct.unpack_from('f', data, 277)
			vy = round(vy[0], 3)
			vz = struct.unpack_from('f', data, 281)
			vz = round(vz[0], 3)
			throttle = struct.unpack_from('f', data, 297)
			throttle = round(throttle[0], 3)

			print(airspeed, pitch, roll, yaw, lat, lon, alt, vx, vy, vz)
				
			elevator = pitch*-0.01
			aileron = (roll)*-0.01
			rudder = 0
			message = struct.pack('<4sBi8fi8f', b'DATA', 0, 25, 1, 0, 0, 0, 0, 0, 0, 0, 11, elevator, aileron, rudder, 0, -999, 0, 0, 0)
			sock.sendto(message, (IP_Send, Port_Send))