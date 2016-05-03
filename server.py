'''
server.py
Should act like a normal server
Should not know it is being accessed through onion routing
Should send back the hash of the received message
'''
import socket
import hashlib

TCP_IP = '127.0.0.1'
TCP_PORT = 1601
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1) #maximum 1 connection



while 1:
	conn, addr = s.accept()
	addr = addr[0]
	print 'Connection address:', addr
	data = conn.recv(BUFFER_SIZE)
	hashed = hashlib.sha224(data).hexdigest()
	if not data: break
	print "received data:", data
	conn.send(hashed)  # return hash
conn.close()
