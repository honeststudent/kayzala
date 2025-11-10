# ====== CIPHER PROGRAM ======
# Author: Aditya Kale (for practical / demo use)
# Ciphers: Playfair, Vigenere, Columnar, Rail Fence

import math

# ===================== PLAYFAIR CIPHER =====================

def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()
    for c in key:
        if c not in used and c.isalpha():
            used.add(c)
            matrix.append(c)
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in used:
            matrix.append(c)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j
    return None

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = text.upper().replace("J", "I").replace(" ", "")
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            b = 'X'
            i += 1
        else:
            i += 2
        pairs.append((a, b))

    cipher = ""
    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:
            cipher += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            cipher += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            cipher += matrix[r1][c2] + matrix[r2][c1]
    return cipher

def playfair_decrypt(cipher, key):
    matrix = generate_playfair_matrix(key)
    cipher = cipher.upper().replace(" ", "")
    plain = ""
    for i in range(0, len(cipher), 2):
        a, b = cipher[i], cipher[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:
            plain += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            plain += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            plain += matrix[r1][c2] + matrix[r2][c1]
    return plain

# ===================== VIGENERE CIPHER =====================

def vigenere_encrypt(text, key):
    text, key = text.upper(), key.upper()
    cipher = ""
    for i, ch in enumerate(text):
        if ch.isalpha():
            cipher += chr((ord(ch) + ord(key[i % len(key)]) - 2*ord('A')) % 26 + ord('A'))
        else:
            cipher += ch
    return cipher

def vigenere_decrypt(cipher, key):
    cipher, key = cipher.upper(), key.upper()
    plain = ""
    for i, ch in enumerate(cipher):
        if ch.isalpha():
            plain += chr((ord(ch) - ord(key[i % len(key)]) + 26) % 26 + ord('A'))
        else:
            plain += ch
    return plain

# ===================== COLUMNAR CIPHER =====================

def columnar_encrypt(text, key):
    text = text.replace(" ", "").upper()
    col = len(key)
    row = math.ceil(len(text)/col)
    fill = row*col - len(text)
    text += 'X'*fill
    arr = [text[i:i+col] for i in range(0, len(text), col)]
    order = sorted(range(len(key)), key=lambda x: key[x])
    cipher = ''.join(''.join(row[i] for row in arr) for i in order)
    return cipher

def columnar_decrypt(cipher, key):
    col = len(key)
    row = math.ceil(len(cipher)/col)
    order = sorted(range(len(key)), key=lambda x: key[x])
    arr = ['']*row
    k = 0
    for i in order:
        for r in range(row):
            if k < len(cipher):
                arr[r] += cipher[k]
                k += 1
    plain = ''.join(arr)
    return plain

# ===================== RAIL FENCE CIPHER =====================

def rail_fence_encrypt(text, rails):
    text = text.replace(" ", "")
    fence = [''] * rails
    rail, step = 0, 1
    for ch in text:
        fence[rail] += ch
        if rail == 0: step = 1
        elif rail == rails-1: step = -1
        rail += step
    return ''.join(fence)

def rail_fence_decrypt(cipher, rails):
    pattern = list(range(rails)) + list(range(rails-2, 0, -1))
    pos = sorted(range(len(cipher)), key=lambda x: pattern[x % len(pattern)])
    plain = [''] * len(cipher)
    k = 0
    for i in pos:
        plain[i] = cipher[k]
        k += 1
    return ''.join(plain)

# ===================== MAIN DEMO =====================
if __name__ == "__main__":
    text = input("Enter the text: ")
    key = input("Enter the key: ")

    print("\n--- PLAYFAIR ---")
    c = playfair_encrypt(text, key)
    print("Encrypted:", c)
    print("Decrypted:", playfair_decrypt(c, key))

    print("\n--- VIGENERE ---")
    c = vigenere_encrypt(text, key)
    print("Encrypted:", c)
    print("Decrypted:", vigenere_decrypt(c, key))

    print("\n--- COLUMNAR ---")
    c = columnar_encrypt(text, key)
    print("Encrypted:", c)
    print("Decrypted:", columnar_decrypt(c, key))

    print("\n--- RAIL FENCE ---")
    c = rail_fence_encrypt(text, 3)
    print("Encrypted:", c)
    print("Decrypted:", rail_fence_decrypt(c, 3))
