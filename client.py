import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

TCP_PORT = 8000
BUFFER_SIZE = 4096
DIR_NODE = '127.0.0.1' #change this
dest_ip = input("Destination Address: ")
mes =  input("Message: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((DIR_NODE, TCP_PORT))
s.send('client')
dir_data = s.recv(BUFFER_SIZE)
s.close()

#parse the directory data string
#code goes here
in_keys = []
in_addr = []
dir_arr = dir_data.split(',')
for x in dir_arr:
	if '.' in x:
		in_addr.append(x)
	else:
		in_keys.append(x)

for x in range(0,2):
	pubkeys[x] = in_keys[2-x]
	node_addr[x+1] = in_addr[2-x]
node_addr[0] = dest_ip
def wrap_layers(message, nodes, public_keys):
	for x in range(0,2):
		message = message + nodes[x]
		message = encrypt(message, public_keys[x])
#wrap_layers(MESSAGE)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((node_addr[0], TCP_PORT))
s.send(mes)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data