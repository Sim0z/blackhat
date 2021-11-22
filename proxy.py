#!/bin/python3
import sys
import socket
import threading

#just for representation
ASCII_REP = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

##Getting the Hex Rep
#Decode it from byte format into string format
def hexdump(src, length=16, show=True):
	if isinstance(src, bytes):
		src = src.decode()
#initialize a list
	results = list()
	for i in range (0, len(src), length):
		word = str(src[i:i+length])
		printable = word.translate(ASCII_REP)
		hexa = ' '.join([f'{ord(c):02X}' for c in word])
		hexwidth = length*3
		results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printable}')
	if show:
		for line in results:
			print(line)
	else:
		return results

def receivefrom(connection):
	buffer =b""
	connection.settimeout(10)
	try:
		while True:
			data = connection.recv(4096)
			if not data:
				break
			buffer += data
	except Exception as e:
		print('error', e)
		pass
	return buffer

def requesthandler(buffer):
		return buffer
def responsehandler(buffer):
		return buffer
	

def proxyhandler(clientsocket, remotehost, remoteport, receivefirst):
	remotesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remotesocket.connect((remotehost, remoteport))

	if receivefirst:
		remotebuffer = receivefrom(remotesocket)
		if len(remotebuffer):
			print("** Received %d bytes from remote." %len(remotebuffer))
			hexdump(remotebuffer)

			remotebuffer = responsehandler(remotebuffer)
			clientsocket.send(remotebuffer)
			print("** Sent to local.")

	while True:
		localbuffer = receivefrom(clientsocket)
		if len(localbuffer):
			print("** Received %d bytes from local." %  len(localbuffer))
			hexdump(localbuffer)

			localbuffer = requesthandler(localbuffer)
			remotesocket.send(localbuffer)
			print("** Sent to remote.")

		remotebuffer = receivefrom(remotesocket)
		if len(remotebuffer):
			print("** Received %d bytes from remote." % len(remotebuffer))
			hexdump(remotebuffer)

			remotebuffer = responsehandler(remotebuffer)
			clientsocket.send(remotebuffer)
			print("** Sent to local.")
		if not len(localbuffer) or not len(remotebuffer):
			clientsocket.close()
			remotesocket.close()
			print("** No more data. Connection is closing")
			break
def serverloop(localhost, localport, remotehost, remoteport, receivefirst):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		server.bind((localhost, localport))

	except  Exception as e:
		print("!! Failed to listen on %s:%d" % (localhost, localport))
		print(e)
		sys.exit(0)		


	print("** Listening on %s:%d" % (localhost, localport))
	server.listen(5)
	while True:
		clientsocket, addr = server.accept()
		print("** Received incoming connection from %s:%d" % (addr[0], addr[1]))
		
		proxythread = threading.Thread(
		target=proxyhandler,
		args=(clientsocket, remotehost, remoteport, receivefirst))
		proxythread.start()

def main():
		if len(sys.argv[1:]) != 5:
			print("Usage: ./proxy.py localhost localport", end='')
			print("remotehost remoteport receivefirst")
			print("Example: ./proxy 127.0.0.1 9001 192.168.11.20 8080 True")
			sys.exit(0)
		
		localhost = sys.argv[1]
		localport = int(sys.argv[2])
		remotehost = sys.argv[3]
		remoteport = int(sys.argv[4])
		receivefirst = sys.argv[5]

		if "True" in receivefirst:
			receivefirst = True
		else:
			receivefirst = false

		serverloop(localhost, localport, remotehost, remoteport, receivefirst)






if __name__ == '__main__':
	main()


