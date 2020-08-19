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

def mode_1():
	print("Mode Auto")
	ser.write(chr(97))

def mode_3():
	print("Mode Stabilize")
	ser.write(chr(115))

def mode_2():
	print("Mode Loiter")
	ser.write(chr(108))

def mode_4():
	print("Mode Manual")
	ser.write(chr(109))

def mode():
	while True:
		input = select.select([sys.stdin], [], [], 1)[0]
		if input:
			key = sys.stdin.readline().strip()
			if(key == "1"):
				mode_1()
			elif(key == "2"):
				mode_2()
			elif(key == "3"):
				mode_3()
			elif(key == "4"):
				mode_4()

def receive_udp():
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
				airspeed = round(airspeed[0]*0.514444, 3)
				groundspeed = struct.unpack_from('f', data, 57)
				groundspeed = round(groundspeed[0]*0.514444, 3)
				ax = struct.unpack_from('f', data, 101)
				ax = int(ax[0])
				#ax = round(ax[0]*9.8, 3)
				ay = struct.unpack_from('f', data, 105)
				ay = int(ay[0])
				#ay = round(ay[0]*9.8, 3)
				az = struct.unpack_from('f', data, 97)
				az = int(0 - az[0])
				#az = round((0 - az[0])*9.8, 3)
				gx = struct.unpack_from('f', data, 117)
				gx = round(gx[0]*0.0174533, 3)
				gy = struct.unpack_from('f', data, 121)
				gy = round(gy[0]*0.0174533, 3)
				gz = struct.unpack_from('f', data, 125)
				gz = round(gz[0]*0.0174533, 3)
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
				# Kirim Serial
				data_serial = struct.pack('c3f3h15fc', b'$', timer, airspeed, groundspeed, ax, ay, az, gx, gy, gz, pitch, roll, yaw, mag, lat, lon, alt, x, y, vx, vy, vz, b'\n')
				ser.write(data_serial)
				#print(len(data_serial))

				#print(airspeed, ax, ay, az, gx, gy, gz, pitch, roll, yaw, lat, lon, alt, vx, vy, vz)

def map(x, in_min, in_max, out_min, out_max):
	return float((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)

def read_serial():
	while True:
		data = ser.readline()
		#print(data)
		#print(len(data))
						
		if len(data) == 24:
			header = struct.unpack_from('c', data, 0)
			elevator = struct.unpack_from('f', data, 4)
			elevator = round(elevator[0], 3)
			aileron = struct.unpack_from('f', data, 8)
			aileron = round(aileron[0], 3)
			rudder = struct.unpack_from('f', data, 12)
			rudder = round(rudder[0], 3)
			throttle = struct.unpack_from('f', data, 16)
			throttle = round(throttle[0], 3)
			#print(header)
			print(elevator, aileron, rudder, throttle)
		
			# Kirim UDP
			message = struct.pack('<4sBi8fi8f', b'DATA', 0, 25, throttle, 0, 0, 0, 0, 0, 0, 0, 11, elevator, aileron, rudder, 0, -999, 0, 0, 0)
			sock.sendto(message, (IP_Send, Port_Send))

		#if len(data) == 14:
		#	header = struct.unpack_from('c', data, 0)
		#	elevator = struct.unpack_from('f', data, 1)
		#	elevator = round(elevator[0], 3)
		#	aileron = struct.unpack_from('f', data, 5)
		#	aileron = round(aileron[0], 3)
		#	rudder = struct.unpack_from('f', data, 9)
		#	rudder = round(rudder[0], 3)
			#print(header)
		#	print(elevator, aileron, rudder)
		
			# Kirim UDP
		#	message = struct.pack('<4sBi8fi8f', 'DATA', 0, 25, 1, 0, 0, 0, 0, 0, 0, 0, 11, elevator, aileron, rudder, 0, -999, 0, 0, 0)
		#	sock.sendto(message, (IP_Send, Port_Send))

if __name__ == "__main__":
	Process(target=receive_udp).start()
	Process(target=read_serial).start()
	mode()	

