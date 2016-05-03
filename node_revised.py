'''
node.py
Tasks:
Send info to directory node
Decrypt layer of encryption
Relay data onward
On data coming back, decrypt and send to previous node
'''

import socket
import sys
from os import chmod

DIR_IP = '172.17.224.57'
DIR_PORT = 1600

TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_PORT = 1601

BUFFER_SIZE = 4096 
NODES = {}

def generateKeys():
	RSAKeys = []
	AESKey = ""
	privateKeyFile = "privateRSA.key"
	publicKeyFile = "publicRSA.key"

	if len(sys.argv) == 2 and sys.argv[1] == "-genKey":
		RSAKeys = aes_rsa.genRSAKey()
		with open(privateKeyFile, 'w') as myContent:
			chmod(privateKeyFile, 0600)
			myContent.write(RSAKeys[1])
		with open(publicKeyFile, 'w') as myContent:
			chmod(privateKeyFile, 0600)
			myContent.write(RSAKeys[0])
	
	elif len(sys.argv) == 1:
	    print "importing keys"   
	else:
	    print "Incorrect arguments"
	    sys.exit()

	try:
	    publicRSA = open(publicKeyFile).read()
	    privateRSA = open(privateKeyFile).read()
	    aes = open(aesKeyFile).read()
	except:
	    print "importing keys failed"
	    exit()

	   return publicRSA, privateRSA, aes

def updateDirectory():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((DIR_IP, DIR_PORT))
	s.send('Onion Router,' + myKeys[0])
	s.close()

def getDirectoryData():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, DIR_PORT))
	s.listen(1)

	conn, addr = s.accept()
	addr = addr[0]
	myData = conn.recv(BUFFER_SIZE).split(",")

	print 'Connection address:', addr

	for x in range(1):
   		NODES[myData[2 * x]] = myData[2 * x + 1]

	conn.close()
	s.close()

def runNode(myKeys):
	entranceFlag = ""
	entranceAddr = ""
	exitAddr = ""

	while 1:
		conn, addr = s.accept()
		addr = addr[0]
		data = conn.recv(BUFFER_SIZE)

		print "[Node Running] Connection address: ", addr

		if not data: break
    	print "[Node Running] Received data: ", data

    	myEncryptedData = data.split(",")
    	decryptedMessage = decryptAESRSA(myEncryptedData[1], myKeys[1], myEncryptedData[0]).split(",")
    	nextNode = decryptedMessage[0]

    	# Entrance Node Case
    	if len(decryptedMessage) == 4:
    		entranceFlag = decryptedMessage[3]
    		entranceAddr = addr

    	conn.closeall()
	    s.close()
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    	# Send to Next Node
    	if nextNode in NODES:  
	        s.connect((nextNode, TCP_PORT))
	        s.send(decryptedMessage[1] + "," + decryptedMessage[2])
	        s.close()
	        
	    # Entrance Node
   		elif entranceFlag == "entrance" and not nextNode:
	        s.connect((entranceAddr, TCP_PORT))
	        s.send(decryptedMessage[1] + "," + decryptedMessage[2])
	        s.close()

	        entranceFlag = ""
	        entranceAddr = ""

	    # Exit Node - Send Data Back
	    elif nextNode not in NODES:
	        s.connect((nextNode, TCP_PORT))
	        s.send(decryptedMessage[1])

	        serverResponse = s.recv(BUFFER_SIZE)
	     	
	     	# WORK IN PROGRESS ---- 
	     	# Goal: Encrypt on way back

	     	encryptedOne = easyEncrypt(myKeys[1], decryptedMessage[0] + "," + serverResponse + "," + NODES[decryptedMessage[0]])
	     	encryptedTwo = easyEncrypt(myKeys[1], encryptedOne[0] + "," + encryptOne[1])

	     	# ----------------------

	        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	        s.connect((, TCP_PORT))
	        s.send()
	        s.close()


      	# Continue Listening
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
