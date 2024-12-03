# __________________________________________________________________________#
# __________________________________________________________________________#
# __________________________________________________________________________#


"""
# Example usage of basic function
message = "Bonjour, ceci est un test."
RSA1 = RSA()
RSA2 = RSA()
# RSA1 encrypts a message using RSA2's public key and sign
enc = RSA1.encrypt(message, RSA2.pubk)
signature = RSA1.sign(message)
# RSA2 decrypts the message using its private key and verify
dec2 = RSA2.decrypt(enc)
is_verified = RSA2.verify(message, signature, RSA1.pubk)

# Print the results
print("Message original :", message)
print("Message chiffré (par RSA1 pour RSA2) :", enc)
print("Message déchiffré (par RSA2) :", dec2)
print("Signature :", signature)
print("Signature vérifiée :", "Oui" if is_verified else "Non")
"""

# __________________________________________________________________________#
# __________________________________________________________________________#
# __________________________________________________________________________#


""" 
# Example usage of exporting and importing keys
rsa1 = RSA()
key_file = 'rsa_keys.json'

# Export keys to file
rsa1.export_keys_to_file(key_file)

# Import keys from file and create a new RSA instance
rsa2 = RSA.import_keys_from_file(key_file)

# Test
message = "Bonjour, ceci est un test."
enc = rsa2.encrypt(message, rsa2.pubk)
dec = rsa2.decrypt(enc)
print("Message original:", message)
print("Message chiffré:", enc)
print("Message déchiffré:", dec)
"""


