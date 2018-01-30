import application_logic.dashboard_controller.facade.service.Service
import socket
import fcntl
import struct

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
while 1:
	try:
		conn, addr = s.accept()
		while 1:
		    data = conn.recv(BUFFER_SIZE)
		    if not data: break
		sensorid, trigger = data.decode("utf-8").split(" ")

		if mrHotchins.check_if_sensor_present(sensorid):
			mrHotchins.add_new_device(sensorid)
		if trigger:
			mrHotchins.report_water_damage(sensorid)
		conn.close()
	except:
		conn.close()
