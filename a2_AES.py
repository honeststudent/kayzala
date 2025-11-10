#pip install pycryptodome

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Encryption function
def aes_encrypt(plain_text, key):
    key = key.encode('utf-8')
    plain_text = plain_text.encode('utf-8')
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return iv + cipher_text

# Decryption function
def aes_decrypt(cipher_data, key):
    key = key.encode('utf-8')
    iv = cipher_data[:16]                  
    cipher_text = cipher_data[16:]         
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return plain_text.decode('utf-8')


if __name__ == "__main__":
    key = "thisisasecretkey" 
    text = input("Enter text: ")

    print("Original Text:", text)

    encrypted = aes_encrypt(text, key)
    print("Encrypted (bytes):", encrypted)

    decrypted = aes_decrypt(encrypted, key)
    print("Decrypted Text:", decrypted)