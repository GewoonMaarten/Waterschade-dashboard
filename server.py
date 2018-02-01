"""
This is the scripts which listens to incoming messages for the connected 
devices. When it recieves an message it will first check if its in the 
database. if not, it will at it. if it is then it will report that is 
has detected water damage. 
"""

from application_logic.dashboard_controller.facade.service import Service as DBagent
import socket
import fcntl
import struct
import sys

# def get_ip_address(ifname):
# 	sintern = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	return socket.inet_ntoa(fcntl.ioctl(
# 		sintern.fileno(),
# 		0x8915,
# 		struct.pack('256s', bytes(ifname.encode('utf-8')))
# 	)[20:24])

#TCP_IP = get_ip_address('wlan0')
TCP_IP = "0.0.0.0"
#print(TCP_IP)
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
sys.stderr.write("waiting for data")

DBconnection = DBagent()

while 1:
	conn, addr = s.accept()
	while 1:
		data = conn.recv(BUFFER_SIZE)
		if not data: 
			print("transmission recieved")
			break
		sensorid, trigger = data.decode("utf-8").split(" ")
		print(sensorid, trigger)
		if not DBconnection.check_if_sensor_present(sensorid):
			print("adding sensor to database")
			DBconnection.add_new_device(sensorid)
		print("general check")
		if trigger is not "0":
			print(trigger)
			print("sensor has been triggered")
			DBconnection.report_water_damage(sensorid)
	conn.close()
	print("connection closed")
