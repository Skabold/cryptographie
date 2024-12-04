
# Exemple d'utilisation
from aes import AES


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
