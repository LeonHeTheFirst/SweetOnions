'''
client.py
Client should do the following things in order:
1. Get list of node ip addresses and public keys from directory node
2. Pick a random ordering of 3 of these nodes
3. Get user input for info to send
4. Add encryption layers onto the packet being sent
5. Send onion packet to first node
6. Wait on return packet from the server
7. Compare returned hash to hash of sent packet
8. Repeat from step 3
'''
import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import random
import hashlib

TCP_PORT = 8000
BUFFER_SIZE = 4096
DIR_NODE = '127.0.0.1' #change this
dest_ip = input("Destination Address: ")
mes =  input("Message: ")
mes_hash = hashlib.sha224(mes).hexdigest()
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
i = 0
for x in random.shuffle(range(0,2)):
	pubkeys[i] = RSA.importKey(in_keys[x])
	node_addr[i+1] = in_addr[x]
	i+=1
node_addr[0] = dest_ip

def wrap_layers(message, nodes, public_keys):
	for x in range(0,2):
		message = nodes[x] + ',' + message
		message = public_keys[x].encrypt(message, 32)

wrap_layers(mes, node_addr, pubkeys)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((node_addr[i], TCP_PORT))
s.send(mes)
data = s.recv(BUFFER_SIZE)
s.close()
if data == mes_hash:
	print "Received data matches hash:", data
else
	print "Received data does not match hash:", data
