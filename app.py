import hashlib
import random
import math
from cgitb import text



def key(*args, **kwargs):
    output_alice_pub = Element("output_alice_pub")
    output_alice_prv = Element("output_alice_prv")
    output_bob_pub = Element("output_bob_pub")
    output_bob_prv = Element("output_bob_prv")
    output_ca_pub = Element("output_ca_pub")
    output_ca_prv = Element("output_ca_prv")
    
    e_alice = creer_clef()
    e_bob = creer_clef()
    e_ca = creer_clef()
    
    cle_publique_alice = e_alice[0]
    cle_privee_alice = e_alice[1]
    cle_publique_bob = e_bob[0]
    cle_privee_bob = e_bob[1] 
    cle_publique_ca = e_ca[0]
    cle_privee_ca = e_ca[1]   
    
    
    output_alice_pub.write(cle_publique_alice)
    output_alice_prv.write(cle_privee_alice)
    output_bob_pub.write(cle_publique_bob)
    output_bob_prv.write(cle_privee_bob)
    output_ca_pub.write(cle_publique_ca)
    output_ca_prv.write(cle_privee_ca)
    

def crypt(*args, **kwargs):
    crypt_area = Element('crypt_area')
    output_crypt = Element("output_crypt")
    if crypt_area.element.value == '':
        output_crypt.write("Entrez un message à crypter")
    else :
        crypt_text = encrypt_cesar(crypt_area.element.value,"8")
        output_crypt.write(crypt_text)


def decrypt(*args, **kwargs):
    decrypt_area = Element('decrypt_area')
    output_decrypt = Element("output_decrypt")
    if decrypt_area.element.value == '':
        output_decrypt.write("Entrez un message à décrypter")
    else : 
        decrypt_text = decrypt_cesar(decrypt_area.element.value,"8")
        output_decrypt.write(decrypt_text)
        
def encrypt(char, key):
    if char.isalpha():
        if char.isupper():
            return chr((ord(char) - 65 + key) % 26 + 65)
        else:
            return chr((ord(char) - 97 + key) % 26 + 97)
    else:
        return char


def encrypt_cesar(text, key):
    text = text.lower()
    key = ord(key) - 96
    return ''.join([encrypt(char, key) for char in text])

def decrypt_cesar(text, key):
    text = text.lower()
    key = ord(key) - 96
    return ''.join([encrypt(char, -key) for char in text])
    

def puissance(a, e, n):
    p=1
    while e>0:
        if e%2==1:
            p=(p*a)%n
        a=(a*a)%n
        e=e//2
    return p


def get_random_prime(a, b):
    while True:
        n = random.randint(a, b)
        if test_prime(n):
            return n
   
        
def test_prime(n):   
    if ((puissance(2, n-1, n) == 1) and
        (puissance(3, n-1, n) == 1) and
        (puissance(5, n-1, n) == 1) and
        (puissance(7, n-1, n) == 1) and
        (puissance(11, n-1, n) == 1) and
            (puissance(13, n-1, n) == 1)):
        return True
    return False

def creer_clef():
    p = get_random_prime(10000, 99999)
    q = get_random_prime(10000, 99999)
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(2, phi-1)
    d = bezout(e, phi)[0]
    if d <= 0:
        creer_clef()
    cle_publique = (e, n)
    cle_prive = (d, n)
    return (cle_publique, cle_prive, p,   q,   n,   phi,    e,   d)

def bezout(a, b):
    if b == 0:
        return (1, 0)
    else:
        (u, v) = bezout(b, a % b)
        return (v, u-(a//b)*v)

        
        

        
