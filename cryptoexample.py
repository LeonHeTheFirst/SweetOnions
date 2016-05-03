
import sys
import os
from os import chmod
import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import base64
import ast
import random
import hashlib
import random

msg = '''
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn

'''

BLOCK_SIZE = 16
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
#generate the random key
secret = os.urandom(BLOCK_SIZE)
print "secret: ", base64.b64encode(secret)
#create the encrypter
cipher = AES.new(secret)
#encrypt
encrpytedMsg = EncodeAES(cipher, msg)

key = RSA.generate(2048)

binPrivKey = key.exportKey('PEM')
binPubKey =  key.publickey().exportKey('PEM')

privKeyObj = RSA.importKey(binPrivKey)
pubKeyObj =  RSA.importKey(binPubKey)


eKey = pubKeyObj.encrypt(base64.b64encode(secret), 32)[0]
print eKey
#decrypt the key
dKey = privKeyObj.decrypt(eKey)
print dKey

#Use decrypted AES key to decrypt encrypted message
decrypter = AES.new(base64.b64decode(dKey))
decryptedMsg = DecodeAES(decrypter, encrpytedMsg)
print decryptedMsg



