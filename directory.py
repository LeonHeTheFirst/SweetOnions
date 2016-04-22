# Maintain a list of available nodes (Node Name, IP Address, Public Key) for clients
# to access. Upon request, provide three nodes (entry, onion router, exit) for the client. 
# This should also be able to communicate with the other available nodes and obtain 
# their information (i.e. changing public keys, etc.).

import socket
import random

NUM_ROUTERS = 5

routerCount = 0
onionRoutersDict = {}

# TEST
onionRoutersDict[0] = "131.145.441.0, 454gdgdj44"
onionRoutersDict[1] = "131.150.441.1, sdfsdfds32"
onionRoutersDict[2] = "131.155.441.2, s6fsd34433"
onionRoutersDict[3] = "131.165.441.3, dsfdskk666"
onionRoutersDict[4] = "131.175.441.4, 4454jjjj33"

randomSelection = []

directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
directoryServer.bind((socket.gethostname(), 1600))
print socket.gethostname()
directoryServer.listen(5)

# Begin listening
while 1:
	myClientSocket, myClientAddress = directoryServer.accept()
	dataReceived = myClientSocket.recv(512)
	
	# Initialization: Communicate with all onion routers until all keys are stored.	
	myData = dataReceived.split(",")
	if myData[0].strip() == "Onion Router":
		onionRoutersDict[routerCount] = myClientAddress + ", " + dataReceived[1].strip()
		routerCount = routerCount + 1
		print "Onion Router Information Received [" + myClientAddress + "] - [" + dataReceived + "]"

	# Initialization complete. 
	if dataReceived == "Client Request" and len(onionRoutersDict) == NUM_ROUTERS:

		# Select random routers to choose from.
		while len(randomSelection) != 3:
			randomNum = random.randrange(0, NUM_ROUTERS)
			if randomNum not in randomSelection:
				randomSelection.append(randomNum)

		# Develop and send message.
		message = onionRoutersDict[randomSelection[0]] + ", " + onionRoutersDict[randomSelection[1]] + ", " + onionRoutersDict[randomSelection[2]]
		myClientSocket.send(message)

		randomSelection = []
