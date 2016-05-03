
import sys
from os import chmod
import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import random
import hashlib
import random


key = RSA.generate(2048)

binPrivKey = key.exportKey('PEM')
binPubKey =  key.publickey().exportKey('PEM')

privKeyObj = RSA.importKey(binPrivKey)
pubKeyObj =  RSA.importKey(binPubKey)

msg = "attack at dawn"
emsg = pubKeyObj.encrypt(msg, 32)[0]
print emsg
dmsg = privKeyObj.decrypt(emsg)
print dmsg

assert(msg == dmsg)