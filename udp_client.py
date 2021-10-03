import socket

target_host = "localhost"
target_port = 80

#create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#send some data
client.sendto(b"Hey folk, this is my test data", (target_host,target_port))

#receive the response
data,address = client.recvfrom(4096)
print(data)
