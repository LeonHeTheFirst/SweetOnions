#Written by Austin Chu
#last changed by Austin Chu on April 1st, 2016

import socket

ipList[]
publicKeyList[]

#create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a port
serversocket.bind((socket.gethostname(), 1234))
#become a server socket
serversocket.listen(5)

#get the public keys from the nodes and store them
int x = 0
while 1:
    print "Ready to accept connections\n"
    #accept connections from outside
    connection, address = serversocket.accept()

    #data recieved from connection
    data = connection.recv[1024]
    print "Data recieved\n"
    #if connection is from client, send IPs and public keys
    if data == "client":
        print "Connection to Client, sending IPs and public keys"
    	toBeSent = ', '.join(i + ', ' + j for i,j in zip(ipList,publicKeyList))
    		connection.sendall(toBeSent)

    #else it is a node connection, store public key sent from node
    else:
        print "Connection to node, storing public key"
	    publicKeyList.append(connection.recv[1024])
	    x += 1