# This file contains functions used for multi-layered encryption
import os
import base64
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

BLOCK_SIZE = 16
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

#Generates an AES key
#Returns base64 encoded AES key
def genAESKey():
	secret = os.urandom(BLOCK_SIZE)
	return base64.b64encode(secret)

#Generates an RSA key
#returns a tuple with public key as the first value and private key as the second
def genRSAKey():
	new_key = RSA.generate(2048, e=65537)
    public_key = new_key.publickey().exportKey('PEM') 
    private_key = new_key.exportKey('PEM') 
    return (public_key, private_key)

#Encrypts using AES
#Arguments are the key, then the message
#returns the encrypted message
def encryptAES(key, msg):
	cipher = AES.new(base64.b64decode(key))
	encryptedMsg = EncodeAES(cipher, msg)
	return encryptedMsg

#Decrypts using AES
#Arguments are the key, then the encrypted message
#returns the decrypted message
def decryptAES(key, msg):
	decrypter = AES.new(base64.b64decode(key))
	decryptedMsg = DecodeAES(decrypter, msg)
	pass

#Encrypts using RSA public key
#Arguments are public key and message
#returns encrypted message
def encryptRSA(pubKey, msg):
	pubKeyObj =  RSA.importKey(pubKey)
	encryptedMsg = pubKeyObj.encrypt(msg, 32)[0]
	return encryptedMsg

#Decrypts using RSA private key
#Arguments are private key and encrypted message
#returns decrypted message
def decryptRSA(privKey, msg):
	privKeyObj = RSA.importKey(privKey)
	decryptedMsg = privKeyObj.decrypt(msg)
	return decryptedMsg

#Encrypts using both AES and RSA
#Arguments are AES key, then RSA public key, then message
#returns tuple containing encrypted AES key, then encrypted message
def encryptAESRSA(aesKey, rsaKey, msg):
	encryptedMsg = encryptAES(aesKey, msg)
	encryptedKey = encryptRSA(rsaKey, aesKey)
	return (encryptedKey, encryptedMsg)

#Decrypts using both AES and RSA
#Arguments are encrypted AES key, then RSA private key, then encrypted message
#returns the decrypted message
def decryptAESRSA(aesKey, rsaKey, msg):
	decryptedKey = decryptRSA(rsaKey, aesKey)
	decryptedMsg = decryptAES(decryptedKey, msg)
	return decryptedMsg

#Encrypts using both AES and RSA after generating the AES key itself
#Arguments are RSA public key, then message
#returns tuple containing encrypted AES key, then encrypted message
def easyEncrypt(rsaKey, msg):
	return encryptAESRSA(genAESKey(), rsaKey, msg)
