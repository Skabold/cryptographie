from rsa.rsa_send import send_message  # This assumes the send_message function is defined in send.py
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
