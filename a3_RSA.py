
def gcd(a, b):
    """Find Greatest Common Divisor"""
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Find modular inverse of e under mod phi"""
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None


p = 17
q = 11

n = p * q

phi = (p - 1) * (q - 1)


e = 7  # must be coprime with phi


d = mod_inverse(e, phi)

print("Public Key: (", e, ",", n, ")")
print("Private Key:", d)


msg = int(input("Enter the message (number) to encrypt: "))


cipher = pow(msg, e, n)
print("Encrypted message:", cipher)


plain = pow(cipher, d, n)
print("Decrypted message:", plain)
