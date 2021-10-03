import socket
 
target_host = "localhost"
target_port = 80
 
 #create a socket object
 #The AF_INET parameter is saying we are going to use a standard IPv4 address or hostname.
 #SOCK_STREAM indicates that this will be a TCP client.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the client
client.connect((target_host,target_port))

#send some data , make it as byte string
client.send(b"GET / HTTP/1.1\r\n\nHOST:google.com\r\n\r\n")

#Receive the response
response = client.recv(4096)
print(response)
 
 
