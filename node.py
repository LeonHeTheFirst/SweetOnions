'''
node.py
Tasks:
Send info to directory node
Decrypt layer of encryption
Relay data onward
On data coming back, decrypt and send to previous node
'''
import sys
from os import chmod
import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

DIR_IP = '127.0.0.1'
DIR_PORT = 1600

TCP_IP = '127.0.0.1'
TCP_PORT = 1601
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
private_key_file = "private.key"
public_key_file = "public.key"
NODES = {}

# when the command line argument for generating a key pair is passed
if len(sys.argv) == 2 and sys.argv[1] == "key":
    new_key = RSA.generate(2048, e=65537) 
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM") 
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


##### TALK TO DIR NODE
pub = open(public_key_file, "r").read()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((DIR_IP, DIR_PORT))
s.send('Onion Router,' + pub)
s.close()

key = open(private_key_file, "r").read()
rsakey = RSA.importKey(key)

#listen to directory to fill dictionary
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((DIR_IP, DIR_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    data = conn.recv(BUFFER_SIZE)
    decrypted = rsakey.decrypt(data)
    dataArr = decrypted.split(",")
    NODE = {dataArr[0]:dataArr[1]}
    x = 2
    while x < 9:
        NODE.update({dataArr[x]:dataArr[x+1]})
        x = x + 2


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
        s.connect((nextNode, TCP_PORT))
        s.send(payload)
        s.close()
        
        #listen on that port again
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        #conn.send(data)  # echo
    #last node
    else:
        #sending it off to next guy
        conn.closeall()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((nextNode, TCP_PORT))
        s.send(payload)
        s.close()
        
        #listen on that port again
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        #sending data back
        #write code here


        conn.close()

#if final node case
#
