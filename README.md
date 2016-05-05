# SweetOnions - Making Onion Routing Great Again
------
The purpose of SweetOnions is to emulate a smaller-scale version of onion routing using Python 2.7. There will be a client, server, directory, and three onion routing nodes through which the client can send and recieve encrypted messages. Each message uses asymmetric encryption - the message itself is encrypted with 192-bit AES and the AES key is subsequently encrypted with 2048-RSA to ensure the sender is anonymized. 

## Installation
------
Requires pycrypto and Python 2.7

## Usage
------
This tool requires a minimum of five machines (2 onion routing nodes) and six machines (3 onion routing nodes) to operate in order to simulate a TOR/onion routing network. The machines should be running as follows:

_Machine 1_: python client.py (This will request the user to enter the directory node's IP address as well as the message the user would like to send)

_Machine 2_: python directory.py

_Machine 3_: python node.py -genKey

_Machine 4_: python node.py -genKey

_Machine 5_: python node.py -genKey (Each node will request the directory node's IP address) [Optional Machine]

_Machine 6_: python server.py

## How it Works
------
The following is a breakdown of what each aspect of the project accomplishes. 

### 1. client.py
------
This is the front-end tool that allows users to send and recieve messages from the server. Upon recieving the message from the server, the client will compare the hashes of the sent and recieved messages to ensure integrity. 

The client must first contact the directory node in order to recieve a list of potential onion routing nodes and their RSA public keys. The client will randomly select the path through which the message will be sent, and it will encrypt the message in the following manner, where Node 3 is the exit node and Node 1 is the entrance node:

a) AES Encrypt via Node 3's AES Key the following: [message + Node3_IP]

b) RSA Encrypt Node 3's AES Key with Node 3's public RSA key: [Node3_AESKey]

c) Concatenate the two encrypted messages - this is the inner most layer and the process will repeat two more times.

By the end of the encryption scheme, the following is the result:

_Layer 1_: AES[message + DestinationIP] + RSA[Node3_AESKey]

_Layer 2_: AES[AES[message + DesinationIP] + RSA[Node3_AESKey] + Node3_IP] + RSA[Node2_AESKey]

_Layer 3_: AES[AES[AES[message + DestinationIP] + RSA[Node3_AESKey] + Node2_IP] + RSA[Node2_AESKey] + Node1_IP] + RSA[Node1_AESKey]

It is the each node's responsibility to unwrap each layer via its RSA private key and continue to send the message along.

### 2. directory.py
------
The directory node is designed to send the client (upon request) the list of node IP's and their corresponding public RSA keys. Before the client can make a valid request to the directory node, each onion routing node must first send its IP and its RSA public key to the directory - this is an initialization phase.

### 3. node.py
------
This represents each onion routing node (and has cases for both entrance and exit nodes) and must unwrap one layer of encryption and send the message along. The decryption occurs as follows:

_Message Sent to Node_: AES[AES[message + DesinationIP] + RSA[Node3_AESKey] + Node3_IP] + RSA[Node2_AESKey]

Node 2 uses its private RSA key to obtain the AES Key, and then uses that AES Key to encrypt the remaining contents. The result is:

_Message Node 2 Sends to Node 3_: AES[message + DesinationIP] + RSA[Node3_AESKey]

### 4. server.py
------
The purpose of server is to simply recieve messages and send the hashed version of the message back to the original exit node. 
