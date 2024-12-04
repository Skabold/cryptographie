from aes import AES
from aes_send import send_message

aes1 = AES()
message_to_send = "This is a secret message!"
encrypted_message, mac = send_message("aes_keys.json", message_to_send)

aes1.export_key_to_file("aes_keys.json")
aes2 = AES.import_key_from_file("aes_keys.json")

# 4. Receive and verify the message using AES2 (check the MIC and decrypt)
received_message = aes2.receive(encrypted_message, mac)

# The received message should match the original message
assert received_message == message_to_send
print("Decryption successful. The original message was:", received_message)
