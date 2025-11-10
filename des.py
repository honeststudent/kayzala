from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

key = b'8bytekey'

cipher_encrypt = DES.new(key, DES.MODE_ECB)

msg = input("Enter message to encrypt: ")
msg_bytes = msg.encode()

padded_msg = pad(msg_bytes, DES.block_size)

encrypted = cipher_encrypt.encrypt(padded_msg)
print("Encrypted:", encrypted)

cipher_decrypt = DES.new(key, DES.MODE_ECB)
decrypted_padded = cipher_decrypt.decrypt(encrypted)
decrypted = unpad(decrypted_padded, DES.block_size).decode()

print("Decrypted:", decrypted)
