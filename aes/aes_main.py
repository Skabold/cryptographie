from aes import AES
from aes_send import send_message



message_to_send = "This is a secret message!"
sender_keys_file = 'aes_keys.json'

# Encrypt the message and generate the hash
encrypted_message, mac = send_message(sender_keys_file, message_to_send)

aes = AES.import_key_from_file("aes_keys.json")
aes.decrypt(encrypted_message)
msg, isOk = aes.receive(encrypted_message,mac)
print(msg)
print(isOk)
