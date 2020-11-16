import socketio
import json

sio = socketio.Client()#logger=True, engineio_logger=True)
#sio = socketio.Client()

#@sio.event(namespace='/lukemcdaniel')
#def message(data):
#	print('received message: ' + data)

@sio.event(namespace='/lukemcdaniel')
def connect():
	print("I am connected to the namespace /lukemcdaniel")
	#messageProtocol()

# right after connection success
#@sio.on('on_connect', namespace='/lukemcdaniel')
#def on_on_connect():
#	print('namespace on_connect: ', msg)
#	sio.emit('espClientUsername', 'lukemcdaniel', namespace='/lukemcdaniel')
#	sio.emit('espClientEmail', 'lmcdaniel1998@gmail.com', namespace='/lukemcdaniel')

#data = {"namespace":self.ns, "sid":request.sid, "master":self.master}
        #print(data)
        #socketio.emit('on_connect', data, namespace=self.ns)

@sio.event(namespace='/lukemcdaniel')
def on_connect(msg):
	print('on_connect')
	passcode = input("enter passcode for namespace")
	print('namespace on_connect: ', msg)
	if msg["master"] is True:
		print('master exists')
		print(passcode)
		verifyData = {"namespace":"/lukemcdaniel", "passcode":passcode, "sid":msg["sid"]}
		sio.emit('espTryVerify', verifyData, namespace='/lukemcdaniel')
		print('msg sent')


@sio.on('espClientVerified', namespace='/lukemcdaniel')
def on_espClientVerified(msg):
	print(msg)
	#verMsg = json.loads(msg)
	if msg["verified"] is True:
		print('im verified as: ' + msg["sid"])
		messageProtocol()

@sio.on('server_to_esp', namespace='/lukemcdaniel')
def on_server_to_esp(msg):
	#print('in server -> esp')
	print('\b\b\b\b\b\breceived: ' + msg + '\nsend: ')
	if msg == 'disconnect':
		sio.disconnect(namespace='/lukemcdaniel')

@sio.event(namespace='/lukemcdaniel')
def disconnect():
	print("I am disconnected!")
	exit(0)

def messageProtocol():
	while (1):
		my_message = input("send: ")
		sio.emit('esp_to_server', my_message, namespace='/lukemcdaniel')

def main():
	sio.connect('http://localhost:5000', namespaces=['/lukemcdaniel'])
	#messageProtocol()

if __name__ == "__main__":
	main()