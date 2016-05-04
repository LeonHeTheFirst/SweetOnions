

from aes_rsa import *
msg = '''
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn
attack at dawn

'''

pubKey, privKey = genRSAKey()
print "Public Key: " + pubKey
print "\n\n\n\n"
print "Private Key: " + privKey

aesKey = genAESKey()
print aesKey
encryptedKey, encrpytedMsg = encryptAESRSA(aesKey, pubKey, msg)

print "Encrypted Key: " + encryptedKey

print "Encrypted Message: " + encrpytedMsg

decryptedMsg = decryptAESRSA(encryptedKey, privKey, encrpytedMsg)

print decryptedMsg



