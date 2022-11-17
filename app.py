import hashlib
import random
import math

def key(*args, **kwargs):
    output_alice = Element("output_alice")
    output_alice.write("Les differentes clés on été générées")

def crypt(*args, **kwargs):
    crypt_area = Element('crypt_area')
    output_crypt = Element("output_crypt")
    if crypt_area.element.value == '':
        output_crypt.write("Entrez un message à crypter")
    else : 
        output_crypt.write(crypt_area.element.value)


def decrypt(*args, **kwargs):
    decrypt_area = Element('decrypt_area')
    output_decrypt = Element("output_decrypt")
    if decrypt_area.element.value == '':
        output_decrypt.write("Entrez un message à décrypter")
    else : 
        output_decrypt.write(decrypt_area.element.value)