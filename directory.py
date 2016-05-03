# Maintain a list of available nodes (Node Name, IP Address, Public Key) for clients
# to access. Upon request, provide three nodes (entry, onion router, exit) for the client. 
# This should also be able to communicate with the other available nodes and obtain 
# their information (i.e. changing public keys, etc.).

import socket
import random
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

NUM_ROUTERS = 5

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

directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
directoryServer.bind(("127.0.0.1", 1600)) #'127.0.0.1' for testing
print socket.gethostname()
directoryServer.listen(5)

# Begin listening
while len(pubkeyDict) < 5:
	myClientSocket, myClientAddress = directoryServer.accept()
	myClientAddress = myClientAddress[0]
	dataReceived = myClientSocket.recv(1024)
	
	print dataReceived
	# Initialization: Communicate with all onion routers until all keys are stored.	
	myData = dataReceived.split(",")
	if myData[0].strip() == "Onion Router":
		onionRoutersDict[routerCount] = myClientAddress + ", " + myData[1].strip()
		pubkeyDict[myClientAddress] = myData[1].strip() #add to the dictionary
		routerCount = routerCount + 1
		print "Onion Router Information Received [" + myClientAddress + "] - [" + dataReceived + "]"
	elif myData[0].strip() == "Client Request":
		myClientSocket.sendall("Not ready yet")
	myClientSocket.close()

directoryServer.close()

'''
		#send new addition to all nodes
		message = "" + myClientAddress + ":" + myData[1].strip()
		for x in pubkeyDict.keys():
			nodeKey = RSA.importKey(pubkeyDict[x])
			encrypted = nodeKey.encrypt(message)
			
			send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			send.connect((""+x, 1600))
			send.send(encrypted)

		#send dictionary to new node
		message = ""
		for x in pubkeyDict.keys():
			message += "#####" + x + ":" + pubkeyDict[x]
		newNodeKey = RSA.importKey(myData[1].strip())
		encrypted = newNodeKey.encrypt(message)
		directoryServer.closeall()
		directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		directoryServer.connect((myClientAddress, 1600))
		directoryServer.send(encrypted)
		directoryServer.close()
		
		directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		directoryServer.bind(("127.0.0.1", 1600)) #'127.0.0.1' for testing 
		directoryServer.listen(5)
		'''			      

message = ""                                                 
for x in pubkeyDict.keys():                                                                                                
	message += "," + x + "," + pubkeyDict[x]                                                                       
message = message[1:]
for x in pubkeyDict.keys():
	nodeKey =  RSA.importKey(pubkeyDict[x])
	encrypted = nodeKey.encrypt(message)
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                        
	conn.connect((x, 1600))                                                                           
	conn.send(encrypted)                                                                                            
	conn.close()                                                                                                    


directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
directoryServer.bind(("127.0.0.1", 1600)) #'127.0.0.1' for testing
#print socket.gethostname()
directoryServer.listen(5)

while 1:
	myClientSocket, myClientAddress = directoryServer.accept()
	myClientAddress = myClientAddress[0]
        dataReceived = myClientSocket.recv(1024)
	
	myData = dataReceived.split(",")
	# Initialization complete. 
	if "Client Request" == myData[0]:

		# Select random routers to choose from.
		while len(randomSelection) != 3:
			randomNum = random.randrange(0, NUM_ROUTERS)
			if randomNum not in randomSelection:
				randomSelection.append(randomNum)

		# Develop and send message.
		ips = pubkeyDict.keys()
		keys = pubkeyDict.values()
		message = ips[randomSelection[0]] + "," + keys[randomSelection[0]] + ","
		message += ips[randomSelection[1]] + "," + keys[randomSelection[1]] + ","
		message += ips[randomSelection[2]] + "," + keys[randomSelection[2]]
		#encrypt message by importing client's public key
		clientKey = RSA.importKey(myData[1])
		encryptedMessage = clientKey.encrypt(message)
		myClientSocket.send(encrypedMessage)
		myClientSocket.close()

directoryServer.close()

'''
	elif "Node Request" in dataReceived and len(onionRoutersDict) == NUM_ROUTERS:
		pass
'''
