from rsa import RSA

def send_message(dest_pubk, sender_keys_file, message):
    # Create a new RSA instance and import the sender's keys from the file
    rsa1 = RSA.import_keys_from_file(sender_keys_file)
    
    # Encrypt the message using the recipient's public key
    enc = rsa1.encrypt(message, dest_pubk)
    
    # Generate a SHA-256 hash of the message
    generated_hash = rsa1.generate_hash(message)
    
    # Sign the message using the sender's private key
    signature = rsa1.sign(message)
    
    return enc, signature, generated_hash
