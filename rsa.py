import sympy

def generate_prime(bits=16):
    return sympy.randprime(2**(bits-1), 2**bits)

def mod_inverse(e, phi):
    return pow(e, -1, phi)

def generate_keys():
    p = generate_prime()
    q = generate_prime()

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537
    d = mod_inverse(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

def encrypt(message, public_key):
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in message]

    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    number_list = list(map(int, ciphertext.split(",")))

    return ''.join([chr(pow(char, d, n)) for char in number_list])
