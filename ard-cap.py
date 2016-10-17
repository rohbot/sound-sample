import serial
import OSC
import time
send_address = '127.0.0.1' , 9995
c = OSC.OSCClient()
c.connect(send_address)

ser = serial.Serial('/dev/ttyACM0', 115200)


last_static = time.time()
static_state = 0

def sendMessage(address, value):
	msg = OSC.OSCMessage()
	msg.setAddress(address)
	msg.append(value)
	c.send(msg)
	print msg

sendMessage('/static',0)

while True:
	line  = ser.readline().strip()
	val = ord(line[0])

	if val == ord('@'):
		val = int(line[1:])
		print val
		sendMessage('/pot',val)
	
	elif val == ord('*'):
		sendMessage('/static',1)

	elif val == ord('#'):
		sendMessage('/static',0)
			

	elif val > 96:
		note = val - 97
		print 'off',  note
		sendMessage('/btn'+ str(note) + '/0',0)

	elif val < 78:
		note = val - 65 
		print 'on', note
		sendMessage('/btn'+ str(note) + '/1', 1)

	
		
