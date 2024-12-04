import base64
from aes import AES

def send_message(keys_file, message):
    """
    Encrypt the message using AES and generate a hash of the key + message (concatenated).

    :param keys_file: (str) Path to the file where the sender's AES key is stored.
    :param message: (str) The message to encrypt.
    :return: (tuple) Encoded message and the generated hash.
    """
    # Create a new AES instance and import the sender's key from the file
    aes1 = AES.import_key_from_file(keys_file)
    
    # GET THE KEY VALUE
    key = aes1.key  
    key_str = base64.b64encode(key).decode('utf-8')
    # Encrypt the message
    enc = aes1.encrypt({"message": message})
    
    # Generate the hash using the AES key and the concatenated message
    generated_hash = aes1.generate_hash(key_str + message)
    
    return enc, generated_hash
