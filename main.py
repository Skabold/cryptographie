from hashPKDF.hash import get_pkfd
from rsa.rsa import RSA

clefAES = get_pkfd()
RSA1 = RSA()
RSA2 = RSA()
# RSA1 encrypts a message using RSA2's public key and sign
enc = RSA1.encrypt(clefAES, RSA2.pubk)
signature = RSA1.sign(clefAES)
# RSA2 decrypts the message using its private key and verify
decryptedAESKey = RSA2.decrypt(enc)
is_verified = RSA2.verify(clefAES, signature, RSA1.pubk)

# print(decryptedAESKey)


