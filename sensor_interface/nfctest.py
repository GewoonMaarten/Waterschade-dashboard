from pirc522 import RFID
import time

rdr = RFID()

while True:
	rdr.wait_for_tag()
	(error, tag_type) = rdr.request()
	if not error:
		print("Tag detected")
		(error, uid) = rdr.anticoll()
		if not error:
			print("UID: " + str(uid))
			if not rdr.select_tag(uid):
				if not rdr.card_auth(rdr.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
					print("reading block 10 " + str(rdr.read(10)))
	
# Calls GPIO cleanup
rdr.cleanup()
