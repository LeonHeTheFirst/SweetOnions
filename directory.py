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

NUM_ROUTERS = 3
NUM_NODES = 3

routerCount = 0
#onionRoutersDict = {}

# TEST
#onionRoutersDict[0] = "131.145.441.0, 454gdgdj44"
#onionRoutersDict[1] = "131.150.441.1, sdfsdfds32"
#onionRoutersDict[2] = "131.155.441.2, s6fsd34433"
#onionRoutersDict[3] = "131.165.441.3, dsfdskk666"
#onionRoutersDict[4] = "131.175.441.4, 4454jjjj33"
pubkeyDict = {}
randomSelection = []

DIR_IP = socket.gethostbyname(socket.gethostname())
#DIR_IP = "127.0.0.1"

directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
directoryServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
directoryServer.bind((DIR_IP, 1600)) #'127.0.0.1' for testing
print socket.gethostname()
directoryServer.listen(5)

# Begin listening
while routerCount < NUM_ROUTERS:
	myClientSocket, myClientAddress = directoryServer.accept()
	myClientAddress = myClientAddress[0]
	dataReceived = myClientSocket.recv(1024)
	print(myClientAddress)
	print(dataReceived)
	# Initialization: Communicate with all onion routers until all keys are stored.	
	myData = dataReceived.split("###")
	if myData[0].strip() == "Onion Router":
		#pubkeyDict[routerCount] = myClientAddress + ", " + myData[1].strip()
		pubkeyDict[myClientAddress] = myData[1].strip() #add to the dictionary
		routerCount = routerCount + 1
		print "Onion Router Information Received [" + myClientAddress + "] - [" + dataReceived + "]"
	elif myData[0].strip() == "Client Request":
		myClientSocket.send("Not ready yet")
	print(pubkeyDict)
	myClientSocket.close()
print(pubkeyDict)

directoryServer.close()
time.sleep(1)

#sending serialized dictionary to all nodes
message = ""                                                 
for x in pubkeyDict.keys():                                                                                                
	print(pubkeyDict.keys())
	message += "###" + str(x) + "###" + str(pubkeyDict[x])
message = str(NUM_ROUTERS) + "###" + message[3:]
for x in pubkeyDict.keys():
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                        
	conn.connect((str(x), 1600))                                                                           
	conn.send(message)                                                                                            
	conn.close()                                                                                                    

time.sleep(1)

directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
directoryServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
while (1):
	try:
		directoryServer.bind((DIR_IP, 1600)) #'127.0.0.1' for testin
		break
	except:
		pass
#print socket.gethostname()
directoryServer.listen(5)

while 1:
	myClientSocket, myClientAddress = directoryServer.accept()
	myClientAddress = myClientAddress[0]
        dataReceived = myClientSocket.recv(1024)
	
	myData = dataReceived.split("###")
	# Initialization complete. 
	if "Client Request" == myData[0]:

		# Select random routers to choose from.
		'''
		while len(randomSelection) != NUM_NODES:
			randomNum = random.randrange(0, NUM_ROUTERS)
			if randomNum not in randomSelection:
				randomSelection.append(randomNum)
		
		# Develop and send message.
		ips = pubkeyDict.keys()
		keys = pubkeyDict.values()
		
		message = ""
		for x in range(NUM_NODES):
			message += "###" + ips[randomSelection[x]] + "###" + keys[randomSelection[x]]
		
		message = message[3:]
                #encrypt route by importing client's public key
		
		clientKey = RSA.importKey(myData[1])
		
		aesKey = genAESKey()
		print("AES KEY ######################")
		print(aesKey)
		print("ENCRYPTED MESSAGE")
		encryptedMsg = encryptAES(aesKey, message)
		print(encryptedMsg)
		encryptedKey = clientKey.encrypt(aesKey, 32)[0]
		toSend = encryptedMsg + "###" +encryptedKey
		myClientSocket.send(toSend)
		myClientSocket.close()
		'''
		myClientSocket.send(message)
		myClientSocket.close()

directoryServer.close()
