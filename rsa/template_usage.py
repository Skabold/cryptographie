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

# __________________________________________________________________________#
# __________________________________________________________________________#
# __________________________________________________________________________#

"""
from send import send_message  # This assumes the send_message function is defined in send.py
from rsa import RSA

# Initialize RSA instance (as both sender and receiver)
rsa_instance = RSA.import_keys_from_file('rsa_keys.json')  # Load your public and private keys

# Message to be sent
message = "Hello, this is a secure message!"

# Sender's public key (your own public key since you are the sender)
dest_pubk = rsa_instance.pubk

# Example of encrypting, signing, and generating a hash
enc, signature, generated_hash = send_message(dest_pubk, 'rsa_keys.json', message)

# Now, use the receive method to decrypt the message, verify the signature, and check integrity
decrypted_message, is_verified, hash_matches = rsa_instance.receive(enc, signature, generated_hash)

# Output the results
print("Decrypted message:", decrypted_message)
print("Signature verified:", is_verified)
print("Hash matches:", hash_matches)
"""