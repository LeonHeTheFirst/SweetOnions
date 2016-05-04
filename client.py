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
import sys
from os import chmod
import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import random
import hashlib
import base64
from aes_rsa import *

#NUM_NODES = 3
DIR_PORT = 1600
TCP_PORT = 1601
BUFFER_SIZE = 4096
DIR_NODE = '172.17.224.57' #change this

TCP_IP = socket.gethostbyname(socket.gethostname())

'''
private_key_file = "private.key"
public_key_file = "public.key"


# when the command line argument for generating a key pair is passed
if len(sys.argv) == 2 and sys.argv[1] == "-genKey":
    new_key = RSA.generate(2048, e=65537) 
    public_key = new_key.publickey().exportKey('PEM') 
    private_key = new_key.exportKey('PEM') 
    with open(private_key_file, 'w') as content_file:
        chmod(private_key_file, 0600)
        content_file.write(private_key)
    with open(public_key_file, 'w') as content_file:
        content_file.write(public_key)
elif len(sys.argv) == 1:
    print "importing keys"
    
else:
    print "Incorrect arguments"
    sys.exit()

try:
    key_file = open(private_key_file, "r").read()
    rsakey = RSA.importKey(key_file)
    #print("rsa prive key: " + rsakey)
    ownpubkey = open(public_key_file, "r").read()
    print(ownpubkey)
    #ownpubkey = rsakey.publickey().exportKey('PEM')
except:
    print "failed to import keys"
    exit()
'''
DIR_NODE = raw_input("Directory server to connect to: ")
mes_hash = hashlib.sha224(mes).hexdigest()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((DIR_NODE, DIR_PORT))
while 1:
	s.send('Client Request###')# + ownpubkey)
	dir_data = s.recv(BUFFER_SIZE)
        print(dir_data)
	if dir_data and "Not ready yet" in dir_data: 
            print("directory server not ready")
            exit()
        else:
            break
	#sleep(1)
s.close()

dest_ip = raw_input("Destination Address: ")
mes =  raw_input("Message: ")

#encMsg, encKey = dir_data.split("###")

#decryptedKey = decryptRSA(key_file, encKey)
#print("ARGUMENTS")
#print(encMsg)
#print(decryptedKey)
#decryptedMsg = decryptAES(decryptedKey, encMsg)
#print(decryptedMsg)


dir_arr = dir_data.split("###")
NUM_ROUTERS = dir_arr[0]
dir_arr = dir_arr[1:]

#parse the directory data string
#code goes here
in_keys = []
in_addr = []
#dir_arr = decryptedMsg.split('###')
print("RECEIVED")
print(dir_arr)
for x in range(len(dir_arr)/2):
    '''
    if '.' in x:
        in_addr.append(x)
    else:
        in_keys.append(x)
        '''
    in_addr.append(dir_arr[2*x])
    in_keys.append(dir_arr[2*x + 1])


NUM_NODES = random.randint(2, NUM_ROUTERS)
##SHUFFLE NODES AGAIN
i = 0
y = range(NUM_ROUTERS)
random.shuffle(y)
pubkeys = []
node_addr = [dest_ip]
print(in_keys)
print(in_addr)
#for x in y:
while i < NUM_NODES:
    pubkeys.append(in_keys[y[i]])
    node_addr.append(in_addr[y[i]])
    i+=1


print("UP TO WRAPPING LAYERS")
# front of nodes is server ip, back of nodes is entrance node
def wrap_layers(message, nodes, public_keys):
    for x in nodes[1:]:
        message += "###" + x
        #message = message + ',' + nodes[0]# + ',' + nodes[1] + ',' + nodes[0]
    for x in range(len(nodes) - 1):
        message = nodes[x] + '###' + message
        if x == len(nodes) - 2:
            message = message + '###' + 'entrance'

        encryptedKey, encryptedMsg = easyEncrypt(public_keys[x], message)
        message = encryptedMsg + "###" + encryptedKey
        
    return message

message = wrap_layers(mes, node_addr, pubkeys)

# Send Message
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((node_addr[i], TCP_PORT))
s.send(message)
s.close()

# Recieve Message
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
	conn, addr = s.accept()
        addr = addr[0]
	if addr == node_addr[len(node_addr) - 1]:
		data = conn.recv(BUFFER_SIZE)
		if data == mes_hash:
			print "Received data matches hash: ", data
			break
		else:
			print "Received data does not match hash: ", data
			break

