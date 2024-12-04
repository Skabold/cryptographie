import os
import json
import base64

from aes_utils import *
### Début du TP
# Validate avec https://www.samiam.org/key-schedule.html
class AES:
    def __init__(self, key=None):
        if key is None:
            key = os.urandom(BLOCK_SIZE)
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

# Exemple d'utilisation
cipher = AES(key=bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))

data = {'message': 'Hello, World!'}
encrypted_data = cipher.encrypt(data)
print(f"Encrypted data: {encrypted_data}")
decrypted_data = cipher.decrypt(encrypted_data)
print(f"Decrypted data: {decrypted_data}")


# Exemple d'utilisation use the key from a friend and his message
encoded_key = "56dzKUA2T1LqpleJRKfUzA=="
encrypted_data = b'\xdd\xcb\xbc_k\x91A\x91pw\xe9\x8f\xe0\xe4\xcf\x13\x87\xd0M\xae\xca1\xffJbz\x0b\xb5,~\xe3h\xe6\x17\x8b\xe7S\xa2\x03\xcc\xa4\x08hj\xc4a6a'

# Importer la clé AES
cipher = AES.from_export(encoded_key)
# Déchiffrer le message encodé
decrypted_data = cipher.decrypt(encrypted_data)
print(f"Decrypted data : {decrypted_data}")
