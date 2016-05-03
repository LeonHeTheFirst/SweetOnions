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
BUFFER_SIZE = 4096  # Normally 1024, but we want fast response
private_key_file = "private.key"
public_key_file = "public.key"
NODES = {}

# when the command line argument for generating a key pair is passed
if len(sys.argv) == 2 and sys.argv[1] == "-genKey":
    new_key = RSA.generate(2048, e=65537) 
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM") 
    with open(private_key_file, 'w') as content_file:
        chmod(private_key_file, 0600)
        content_file.write(private_key)
    with open(public_key_file, 'w') as content_file:
        content_file.write(public_key)
if len(sys.argv) == 1:
    try:
        pubkey = open(public_key_file).read()
        privkey = open(private_key_file).read()
        print "importing keys"
    except:
        print "importing keys failed"
        exit()
else:
    print "Incorrect arguments"
    sys.exit()


##### TALK TO DIR NODE
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((DIR_IP, DIR_PORT))
s.send('Onion Router,' + pubkey)
s.close()

privRSAkey = RSA.importKey(privkey)
pubRSAkey = RSA.importKey(pubkey)

#listen to directory to fill dictionary
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((DIR_IP, DIR_PORT))
s.listen(1)

conn, addr = s.accept()
addr = addr[0]
data = conn.recv(BUFFER_SIZE)
decrypted = privRSAkey.decrypt(data)
dataArr = decrypted.split(",")
for x in range(5):
    NODES[dataArr[2 * x]] = dataArr[2 * x + 1]
conn.close()
s.close()        

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

entranceFlag = ""
entranceAddr = ""

print 'Connection address:', addr
while 1:
    conn, addr = s.accept()
    addr = addr[0]
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    decrypted = privRSAkey.decrypt(data)
    dataArr = decrypted.split(",")
    nextNode = dataArr[0]
    payload = dataArr[1]

    if len(dataArr) == 3: 
        entranceFlag = dataArr[2]
        entranceAddr = addr

    if nextNode in NODES:
        #sending it off to next guy
        conn.closeall()
        s.close()
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((nextNode, TCP_PORT))
        s.send(payload)
        s.close()
        
        #listen on that port again
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

    # Entrance Node
    elif entranceFlag == "entrance" and nextNode not in NODES:
        conn.closeall()
        s.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((entranceAddr, TCP_PORT))
        s.send(payload)
        s.close()

        entranceFlag = ""
        entranceAddr = ""

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

    # Exit Node
    # dest, message, node 0, node 1, node 2, ...
    elif nextNode not in NODES and len(dataArr) > 3:
        conn.closeall()
        s.close()
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((nextNode, TCP_PORT))
        s.send(payload)

        data = s.recv(BUFFER_SIZE)
        message = ""
        nextAddr = ""
        for x in range(len(dataArr) - 3):
            nodeKey = RSA.importKey(NODES[dataArr[x+2]])
            temp = nodeKey.encrypt(message, 32)
            if x != len(dataArr) - 4:
                temp += dataArr[x+2]
            else:
                nextAddr = dataArr[x+2]
            message += temp
        
        #message = dataArr[3].encrypt(dataArr[2].encrypt(message, 32), 32)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((nextAddr, TCP_PORT))
        s.send(message)
        s.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)


