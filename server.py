import application_logic.dashboard_controller.facade.service.Service
import socket
import fcntl
import struct

def get_ip_address(ifname):
	sintern = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		sintern.fileno(),
		0x8915,
		struct.pack('256s', bytes(ifname.encode('utf-8')))
	)[20:24])

#TCP_IP = get_ip_address('wlan0')
TCP_IP = "0.0.0.0"
#print(TCP_IP)
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:')
print(addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
	sensorname, bool(trigger) = data.decode("utf-8").split(" ")
    if mrHotchins.check_if_sensor_present(sensorname):
		mrHotchins.add_new_device(sensorname)
	if trigger:
		mrHotchins.report_water_damage(sensorname)
    conn.close()