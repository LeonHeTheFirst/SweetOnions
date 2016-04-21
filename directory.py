# Maintain a list of available nodes (Node Name, IP Address, Public Key) for clients
# to access. Upon request, provide three nodes (entry, onion router, exit) for the client. 
# This should also be able to communicate with the other available nodes and obtain 
# their information (i.e. changing public keys, etc.).

import socket

NUM_ENTRY = 2
NUM_EXIT = 2
NUM_ROUTERS = 5

entryRoutersDict = {}
exitRoutersDict = {}
onionRoutersDict = {}

directoryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
directoryServer.bind((socket.gethostname(), 80))
directoryServer.listen(5)

# Begin listening
while 1:
	myClientSocket, myClientAddress = directoryServer.accept()
	dataReceived = myClientSocket.recv(512)
	
	# Initialization: Communicate with all onion routers until all keys are 
	# stored.	
	if dataReceived == "Onion Router":
		onionRoutersDict[myClientAddress] = dataReceived
		print "Onion Router Information Received [" + myClientAddress + "] - [" + dataReceived + "]"
	else if dataReceived == "Entry Router":
		entryRoutersDict[myClientAddress] = dataReceived
		print "Entry Router Information Received [" + myClientAddress + "] - [" + dataReceived + "]"
	else if dataReceived == "Exit Router":
		exitRoutersDict[myClientAddress] = dataReceived
		print "Exit Router Information Received [" + myClientAddress + "] - [" + dataReceived + "]"

	# Initialization complete. 
	if dataReceived == "Client Request" and len(onionRoutersDict) == NUM_ROUTERS and len(entryRoutersDict) == NUM_ENTRY and len(exitRoutersDict) == NUM_EXIT:
		print "Client Request"
		# Send client data








