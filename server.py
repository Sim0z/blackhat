import socket
import threading    #For multiple connections at the same time :)

ip = '0.0.0.0'      #Listen on all interfaces
port = 80

#the main function
def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((ip, port))
	server.listen(5)
	print(f'[*]Listening on {ip}:{port}')

	while True:
		client,addr = server.accept()
		print(f'[*]Connection Accepted from {addr[0]}:{addr[1]}')
		client_handler = threading.Thread(target=handle_client, args=(client,))
		client_handler.start()
def handle_client(client_socket):
	with client_socket as sock:
		request = sock.recv(1024)
		print(f'[*] Data Received: {request.decode("utf-8")}')
		sock.send(b'Hello My Client')


if __name__ == '__main__':
	main()
