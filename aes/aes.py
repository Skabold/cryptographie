import os
import json
import base64
from aes_utils import *
from hashPKDF.hash import custhash

class AES:
    def __init__(self, key=None):
        if key is None:
            key = os.urandom(BLOCK_SIZE)  # Generate a random key if none is provided
        self.key = key

    def encrypt(self, data):
        """
        Encrypt the data using AES.

        Parameters:
        data (dict): A dictionary containing the data to encrypt.

        Returns:
        bytes: The encrypted data.
        """
        data_bytes = json.dumps(data).encode('utf-8')
        data_bytes = pkcs_pad(data_bytes)

        iv = os.urandom(BLOCK_SIZE)

        data_bytes = list(data_bytes)
        output = b""

        round_keys = generate_round_keys(self.key)
        for b in range(0, len(data_bytes), BLOCK_SIZE):
            if b == 0:
                chainblock = iv
            else:
                chainblock = output[-BLOCK_SIZE:]
            block = data_bytes[b:b+BLOCK_SIZE]

            block = xor_word(block, chainblock)
            block = xor_word(block, round_keys[0])
            for round in range(0, N_ROUNDS):
                round += 1
                block = aes_round(block, round_keys, round)
                assert len(block) == BLOCK_SIZE
            output += block_to_bytes(block)

        return iv + output

    def decrypt(self, data):
        """
        Decrypt the data using AES.

        Parameters:
        data (bytes): The encrypted data to decrypt.

        Returns:
        dict: The decrypted data as a dictionary.
        """
        round_keys = generate_round_keys(self.key)

        lblock = data[-BLOCK_SIZE:]
        lblock = xor_word(lblock, round_keys[-1])
        for round in range(1, N_ROUNDS+1):
            lblock = aes_inv_round(lblock, round_keys, N_ROUNDS - round)

        output = b""
        for b in range(BLOCK_SIZE, len(data), BLOCK_SIZE):
            block = data[-(b+BLOCK_SIZE):-b]

            output = block_to_bytes(xor_word(lblock, list(block))) + output

            lblock = block
            lblock = xor_word(lblock, round_keys[-1])
            for round in range(1, N_ROUNDS+1):
                lblock = aes_inv_round(lblock, round_keys, N_ROUNDS - round)

        output = pkcs_unpad(output)
        return json.loads(output.decode('utf-8'))

    def export(self):
        """Export the AES key as a base64 encoded string."""
        return base64.b64encode(self.key).decode('utf-8')

    @classmethod
    def from_export(cls, encoded_key):
        """Create an AES instance from a base64 encoded key."""
        key = base64.b64decode(encoded_key)
        return cls(key)

    def export_key_to_file(self, filepath):
        """Export the AES key to a JSON file."""
        encoded_key = self.export()
        with open(filepath, 'w') as f:
            json.dump({"key": encoded_key}, f)

    @classmethod
    def import_key_from_file(cls, filepath):
        """Import the AES key from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        encoded_key = data.get("key")
        if encoded_key is None:
            raise ValueError("No key found in the JSON file.")
        return cls.from_export(encoded_key)
    
    
    def generate_hash(self, message):
        """
        Generate a custom hash for the given message using custhash.
        
        :param message: (str) The message to hash.
        :return: (str) The hexadecimal representation of the hash.
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        # Use custhash to generate the hash (bytes format)
        custom_hash_bytes = custhash(message)
        
        # Convert the hash to a hexadecimal string
        custom_hash_hex = custom_hash_bytes.hex()

        return custom_hash_hex
    
    def receive(self, message, mic):
        """
        Verify the message integrity and decrypt the message.

        Parameters:
        message (bytes): The encrypted message to receive.
        mic (str): The message integrity code (hash) to verify the message integrity.

        Returns:
        dict: The decrypted data as a dictionary, if the mic matches.
        """
        
        decrypted_data = self.decrypt(message)
        
        generated_hash = self.generate_hash(self.key + decrypted_data)
        
        print("Decrypted message:", repr(decrypted_data))  # Use repr to see raw byte content
        print("Generated hash of decrypted message:", self.generate_hash(decrypted_data))

        # Check if the generated hash matches the provided mic
        if generated_hash != mic:
            raise ValueError("Message integrity check failed. Mic does not match.")

        return decrypted_data