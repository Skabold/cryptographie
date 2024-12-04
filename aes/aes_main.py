# 1. Create an AES instance (AES1) and encrypt a message
from aes import AES


aes1 = AES()
data_to_encrypt = {"message": "This is a secret message!"}
encrypted_data = aes1.encrypt(data_to_encrypt)
print("Encrypted data:", encrypted_data)

# 2. Export the AES key from AES1 and save it to a JSON file
aes1.export_key_to_file("aes_keys.json")
print("AES key saved to aes_keys.json")

# 3. Import the AES key from the JSON file and create a new AES instance (AES2)
aes2 = AES.import_key_from_file("aes_keys.json")
print("AES key loaded from aes_keys.json")

# 4. Decrypt the message using AES2
decrypted_data = aes2.decrypt(encrypted_data)
print("Decrypted data:", decrypted_data)

# The decrypted data should match the original message
assert decrypted_data == data_to_encrypt
print("Decryption successful. The original message was:", decrypted_data)