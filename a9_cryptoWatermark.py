from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import struct

def encrypt_text(text, password):
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(pad(text.encode(), 16))
    return ct

def decrypt_text(ct_bytes, password):
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ct_bytes), 16)
    return pt.decode()

def embed_payload(image_path, output_path, payload):
    img = Image.open(image_path).convert('RGB')
    w, h = img.size
    pixels = list(img.getdata())
    bits = ''.join(format(b, '08b') for b in payload)
    total_bits = len(bits)
    cap = len(pixels) * 3
    if total_bits > cap:
        raise ValueError("Payload too large for this image.")
    new_pixels = []
    bit_idx = 0
    for (r, g, b) in pixels:
        nr, ng, nb = r, g, b
        if bit_idx < total_bits:
            nr = (r & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < total_bits:
            ng = (g & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < total_bits:
            nb = (b & ~1) | int(bits[bit_idx]); bit_idx += 1
        new_pixels.append((nr, ng, nb))
    img2 = Image.new('RGB', (w, h))
    img2.putdata(new_pixels)
    img2.save(output_path)
    print("Embedded payload ({} bytes) into '{}'".format(len(payload), output_path))

def extract_payload(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = list(img.getdata())
    bits = []
    for (r, g, b) in pixels:
        bits.append(r & 1); bits.append(g & 1); bits.append(b & 1)
    # first 32 bits = 4-byte length
    first32 = bits[:32]
    first_bytes = bytearray()
    for i in range(0, 32, 8):
        byte = 0
        for bit in first32[i:i+8]:
            byte = (byte << 1) | bit
        first_bytes.append(byte)
    (ct_len,) = struct.unpack(">I", bytes(first_bytes))
    total_bits = (4 + ct_len) * 8
    if total_bits > len(bits):
        raise ValueError("Image does not contain the full payload.")
    sel_bits = bits[:total_bits]
    payload = bytearray()
    for i in range(0, total_bits, 8):
        byte = 0
        for bit in sel_bits[i:i+8]:
            byte = (byte << 1) | bit
        payload.append(byte)
    return bytes(payload)  # returns length-prefix + ciphertext

if __name__ == "__main__":
    mode = input("1. Embed\n2. Extract\nEnter choice: ").strip()
    if mode == '1':
        img_in = input("Input image path: ").strip()
        img_out = input("Output image path (include filename, e.g. out.png): ").strip()
        text = input("Watermark text: ").strip()
        pwd = input("Password: ").strip()
        ct = encrypt_text(text, pwd)
        payload = struct.pack(">I", len(ct)) + ct        # 4 bytes length + ciphertext
        embed_payload(img_in, img_out, payload)
        print("Encrypted ciphertext length (bytes):", len(ct))
    elif mode == '2':
        img = input("Stego image path: ").strip()
        pwd = input("Password: ").strip()
        payload = extract_payload(img)
        ct = payload[4:]   # skip first 4 bytes (length)
        try:
            pt = decrypt_text(ct, pwd)
            print("Extracted watermark:", pt)
        except Exception as e:
            print("Decryption failed:", e)
    else:
        print("Invalid choice.")


