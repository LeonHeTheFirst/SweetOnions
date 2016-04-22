'''
node.py
Tasks:
Send info to directory node
Decrypt layer of encryption
Relay data onward
On data coming back, decrypt and send to previous node
'''
import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

DIR_IP = '127.0.0.1'
DIR_PORT = 1600

TCP_IP = '127.0.0.1'
TCP_PORT = 1601
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

NODES = []

##### TALK TO DIR NODE
#pub = open(public_key_file, "r").read()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((DIR_IP, DIR_PORT))
s.send('Onion Router,akjsdhfklajshdkfjash')
s.close()

key = open(private_key_file, "r").read()
rsakey = RSA.importKey(key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print 'Connection address:', addr
while 1:
    conn, addr = s.accept()
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    decrypted = rsakey.decrypt(data)
    dataArr = decrypted.split(",")
    nextNode = dataArr[0]
    payload = dataArr[1]

    if nextNode in NODES:
        #sending it off to next guy
        conn.closeall()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((nextNode, TCP_PORT))
        s.send(payload)
        s.close()
        
        #listen on that port again
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        #conn.send(data)  # echo
        
    else:
        #exit node case
        


        conn.close()

#if final node case
#
