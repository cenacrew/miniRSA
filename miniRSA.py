import hashlib
import random
import math


def puissance(a, e, n):
    if e == 0:
        return 1
    elif e == 1:
        return a % n
    else:
        if e % 2 == 0:
            return puissance(a*a % n, e//2, n)
        else:
            return a * puissance(a*a % n, (e-1)//2, n) % n


def getRandomPrime(a, b):
    while True:
        n = random.randint(a, b)
        if testPrime(n):
            return n


def algoEuclide(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        (d, x, y) = algoEuclide(b, a % b)
        return (d, y, x - (a // b) * y)


def testPrime(n):

    if ((puissance(2, n-1, n) == 1) and
        (puissance(3, n-1, n) == 1) and
        (puissance(5, n-1, n) == 1) and
        (puissance(7, n-1, n) == 1) and
        (puissance(11, n-1, n) == 1) and
            (puissance(13, n-1, n) == 1)):
        return True
    return False

def SHA256(m):
    return hashlib.sha256(m.encode('utf-8')).hexdigest()



def Certificat(n):
    if testPrime(n):
        return "certificat correct"
    else:
        return "certificat incorrect"


def pgcd(a, b):
    if b == 0:
        return a
    else:
        return pgcd(b, a % b)


def bezout(a, b):
    if b == 0:
        return (1, 0)
    else:
        (u, v) = bezout(b, a % b)
        return (v, u-(a//b)*v)

def empreinteCorrectInCorrect(m, cle_publique, cle_prive):
    e = cle_publique[0]
    n = cle_publique[1]
    d = cle_prive[0]
    h = SHA256(m)
    h = int(h, 16)
    s = puissance(h, d, n)
    h2 = puissance(s, e, n)
    h2 = hex(h2)[2:]
    if h == h2:
        return " correcte"
    else:
        return " incorrecte"

def GenererCertificat():
    (cle_publique, cle_prive, p, q, n, phi, e, d) = creer_clef()
    return (cle_publique, cle_prive, p, q, n, phi, e, d, Certificat(n))


def creer_clef():
    p = getRandomPrime(10000, 99999)
    q = getRandomPrime(10000, 99999)
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(2, phi-1)
    d = bezout(e, phi)[0]
    cle_publique = (e, n)
    cle_prive = (d, n)
    return (cle_publique   , cle_prive  , p ,   q   ,   n   ,   phi     ,    e  ,   d)

a = GenererCertificat()
print("Certificat", a)
eAlice = creer_clef()
eCA = creer_clef()
message = "Bonjour"
#empreinte = SHA256(message)
print("2 nombres premiers p et q : " + str(eAlice[2]) + " et " + str(eAlice[3]))
print("n = p * q = " + str(eAlice[4]))
print("phi(n) = " + str(eAlice[5]))
print (eAlice)
print (eCA)
print("public key of Alice e: ", eAlice[0])
print("private key of Alice d: ", eAlice[1] )
print("2 nombres premiers p et q : " + str(eCA[2]) + " et " + str(eCA[3]))
print("n = p * q = " + str(eCA[4]))
print("phi(n) = " + str(eCA[5]))
print("public key of CA e : ", eCA[0])
print("private key of CA  d : " , eCA[1] )
#print("Calcul d'empreinte , ici on utilise empreinte(X)=X%13 :", empreinte)
#print("public key Alice + empreinte : m =" , eAlice[0] , empreinte)
print("message chiffré par CA : " , puissance(eAlice[0][0], eCA[1][0], eCA[1][1]))
print("message déchiffré par Alice : " , puissance(puissance(eAlice[0][0], eCA[1][0], eCA[1][1]), eAlice[1][0], eAlice[1][1]))
print("Empreinte", empreinteCorrectInCorrect(message, eAlice[0], eAlice[1]))
print("génération certificat :" , GenererCertificat())
print("certificat de la clé publique de Alice : ", 0, "= clé publique de Alice " , eAlice[0] , " = certificat de la clé publique de Alice " , Certificat(eAlice[0][1]))
print("Clé publique Alice : " , eAlice[0])
print("Certificat correctIncorrect : " , Certificat(eAlice[0][1]))