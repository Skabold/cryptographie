from aes import AES
from send import send_message

# 1. Create an AES instance (AES1) and encrypt a message
aes1 = AES()
message_to_send = "This is a secret message!"
encrypted_message, mic = send_message("aes_keys.json", message_to_send)
print("Encrypted message:", encrypted_message)
print("Message integrity code (MIC):", mic)

# 2. Export the AES key from AES1 and save it to a JSON file
aes1.export_key_to_file("aes_keys.json")
print("AES key saved to aes_keys.json")

# 3. Import the AES key from the JSON file and create a new AES instance (AES2)
aes2 = AES.import_key_from_file("aes_keys.json")
print("AES key loaded from aes_keys.json")

# 4. Receive and verify the message using AES2 (check the MIC and decrypt)
try:
    received_message = aes2.receive(encrypted_message, mic)
    print("Received and decrypted message:", received_message)
except ValueError as e:
    print("Error:", e)

# The received message should match the original message
assert received_message == message_to_send
print("Decryption successful. The original message was:", received_message)
