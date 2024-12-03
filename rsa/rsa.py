import hashlib
from rsa_utils import get_large_prime_number, eucalg, modpow
import json
import os

class RSA:
    E = 65537
    NBITS = 1024

    def __init__(self):
        self.privk, self.pubk = self.generate_keys(self.NBITS)

    def generate_keys(self, nbits):
        p = get_large_prime_number(nbits // 2)
        q = get_large_prime_number(nbits // 2)
        n = p * q
        lam_n = (p - 1) * (q - 1)
        d = eucalg(self.E, lam_n)[0]
        if d < 0:
            d += lam_n

        pubk = (self.E, n)
        privk = (d, n)
        return privk, pubk

    def encrypt(self, message, pubk):
        """Encrypt a message using a provided public key."""
        message_bytes = message.encode('utf-8')
        number = int.from_bytes(message_bytes, byteorder='big')
        encrypted_number = modpow(number, pubk[0], pubk[1])
        return encrypted_number

    def decrypt(self, encrypted_number):
        """Decrypt a message using the instance's private key."""
        decrypted_number = modpow(encrypted_number, self.privk[0], self.privk[1])
        try:
            message_bytes = decrypted_number.to_bytes((self.pubk[1].bit_length() + 7) // 8, byteorder='big')
            return message_bytes.decode()
        except UnicodeDecodeError:
            return "Erreur : Impossible de décoder en UTF-8."

    def sign(self, message):
        """Sign a message using the instance's private key."""
        message_bytes = message.encode('utf-8')
        number = int.from_bytes(message_bytes, byteorder='big')
        signature = modpow(number, self.privk[0], self.privk[1])
        return signature

    def verify(self, message, signature, pubk):
        """Verify a signature using a provided public key."""
        decrypted_signature = modpow(signature, pubk[0], pubk[1])
        message_bytes = message.encode('utf-8')
        number = int.from_bytes(message_bytes, byteorder='big')
        return decrypted_signature == number

    def export_keys_to_file(self, filepath):
        """Export both public and private keys to a file."""
        keys = {
            'public_key': self.pubk,
            'private_key': self.privk
        }
        with open(filepath, 'w') as f:
            json.dump(keys, f)

    @staticmethod
    def import_keys_from_file(filepath):
        """Import both public and private keys from a file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file {filepath} does not exist.")

        with open(filepath, 'r') as f:
            keys = json.load(f)

        rsa_instance = RSA()
        rsa_instance.pubk = tuple(keys['public_key'])
        rsa_instance.privk = tuple(keys['private_key'])
        return rsa_instance
    
    def generate_hash(self, message):
        """Generate a SHA-256 hash of the message."""
        message_bytes = message.encode('utf-8')
        sha256_hash = hashlib.sha256(message_bytes).hexdigest()
        return sha256_hash
    
    def receive(self, enc, signature, received_hash):
        """Receive an encrypted message, verify the signature, and check the hash for integrity."""
        # Decrypt the message using the private key
        decrypted_message = self.decrypt(enc)
        
        # Strip leading null bytes and whitespace
        decrypted_message = decrypted_message.lstrip('\x00').strip()

        # Verify the signature
        is_verified = self.verify(decrypted_message, signature, self.pubk)
        
        # Generate the hash of the decrypted message to compare with the received hash
        print("Decrypted message:", repr(decrypted_message))  # Use repr to see raw byte content
        print("Generated hash of decrypted message:", self.generate_hash(decrypted_message))
        
        # Print the expected message hash (this should be the same as the received one)
        expected_message = "Hello, this is a secure message!"
        print("Generated hash of expected message:", self.generate_hash(expected_message)) 
        
        hash_matches = (self.generate_hash(decrypted_message) == received_hash)
        
        return decrypted_message, is_verified, hash_matches


