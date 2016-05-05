# Maintain a list of available nodes (Node Name, IP Address, Public Key) for clients
# to access. Upon request, provide three nodes (entry, onion router, exit) for the client. 
# This should also be able to communicate with the other available nodes and obtain 
# their information (i.e. changing public keys, etc.).
import time
import socket
import random
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from aes_rsa import *

NUM_ROUTERS = int(raw_input("Number of routers before running: "))
NUM_NODES = 3

routerCount = 0
pubkeyDict = {}

DIR_IP = socket.gethostbyname(socket.gethostname())

directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
directoryServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
directoryServer.bind((DIR_IP, 1600)) #'127.0.0.1' for testing
directoryServer.listen(5)

print("")
# Begin listening for onion routers
while routerCount < NUM_ROUTERS:
	myClientSocket, myClientAddress = directoryServer.accept()
	myClientAddress = myClientAddress[0]
	dataReceived = myClientSocket.recv(1024)
	print("Connection from: " + myClientAddress)
	
	# Initialization: Communicate with all onion routers until all keys are stored.	
	myData = dataReceived.split("###")
	if myData[0].strip() == "Onion Router":
		
		pubkeyDict[myClientAddress] = myData[1].strip() #add to the dictionary
		routerCount = routerCount + 1
		print "Onion Router Information Received"
		print(myData[1])
		print("")
	
	# If a client connects too early, tell it...
	elif myData[0].strip() == "Client Request":
		myClientSocket.send("Not ready yet")
	myClientSocket.close()

print("Dictionary of nodes:")
for x in pubkeyDict:
	print(x + " : " + pubkeyDict[x])

directoryServer.close()
time.sleep(1)

#Sending serialized dictionary to all nodes
message = ""                                                 
for x in pubkeyDict.keys():
	message += "###" + str(x) + "###" + str(pubkeyDict[x])
message = str(NUM_ROUTERS) + "###" + message[3:]
for x in pubkeyDict.keys():
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                        
	conn.connect((str(x), 1600))                                                                           
	conn.send(message)                                                                                            
	conn.close()                                                                                                    

time.sleep(1)

# Make sure socket is closed
directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
directoryServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
while (1):
	try:
		directoryServer.bind((DIR_IP, 1600)) #'127.0.0.1' for testin
		break
	except:
		pass
	
directoryServer.listen(5)

# Wait for clients to connect
while 1:
	myClientSocket, myClientAddress = directoryServer.accept()
	myClientAddress = myClientAddress[0]
        dataReceived = myClientSocket.recv(1024)
	
	myData = dataReceived.split("###")
	# Initialization complete. 
	if "Client Request" == myData[0]:

		# Send client the dictionary of nodes as well
		myClientSocket.send(message)
	
	myClientSocket.close()

directoryServer.close()
