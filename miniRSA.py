import hashlib
import random
import math


def puissance(a, e, n):
    p = 1
    while e > 0:
        if e % 2 == 1:
            p = (p*a) % n
        a = (a*a) % n
        e = e//2
    return p


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


def SHA256(s):
    return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)


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


def getCertificat(cle_Publique1, cle_Publique2, empreinte, nA, CA):
    Key_part1 = puissance(cle_Publique1, CA[1][0], CA[1][1])
    Key_part2 = puissance(cle_Publique2, CA[1][0], CA[1][1])
    print(CA[1][0], CA[1][1])
    clé_publiqueAlice = str(Key_part1) + " " + str(Key_part2)
    if puissance(empreinte, Key_part1, Key_part2) == SHA256(clé_publiqueAlice) % nA:
        print("clé_publiqueAlice modulo nCA: ", clé_publiqueAlice)
        print("Certificat valide !")
        return (puissance(Key_part1, CA[1][0], CA[1][1]) % nA, puissance(Key_part2, CA[1][0], CA[1][1] % nA))
    else:
        print("Certificat invalide !")
        main()


def creationCertificat(Alice, CApublique):

    messageDeAlice = str(Alice[0][0]) + " " + str(Alice[0][1])
    empreinte = SHA256(messageDeAlice) % Alice[0][1]
    print("empreinte : ", empreinte)
    empreinteSignee = puissance(empreinte, Alice[1][0], Alice[1][1])

    print("Message de Alice ", messageDeAlice)

    message1Chiffre = puissance(Alice[0][0], CApublique[0], CApublique[1])
    message2Chiffre = puissance(Alice[0][1], CApublique[0], CApublique[1])
    return (message1Chiffre, message2Chiffre, empreinteSignee)


def RSA(m, cle_publique):
    partie1 = puissance(m[0], cle_publique[0], cle_publique[1])
    partie2 = puissance(m[1], cle_publique[0], cle_publique[1])
    return (partie1, partie2)


def decryRSA(c, cle_prive):
    partie1 = puissance(c[0], cle_prive[0], cle_prive[1])
    partie2 = puissance(c[1], cle_prive[0], cle_prive[1])
    return (partie1, partie2)


def creer_clef():
    p = getRandomPrime(10000, 99999)
    q = getRandomPrime(10000, 99999)
    n = p*q
    phi = (p-1)*(q-1)
    estPremier = False
    while not estPremier:
        e = random.randint(2, phi-1)
        d = bezout(e, phi)[0]
        if pgcd(e, phi) == 1 and d > 0:
            estPremier = True
    return ((e, n), (d, n), p,   q, e , n)


def main():

    KeyAlice = creer_clef()
    KeyCA = creer_clef()
    KeyBOB = creer_clef()

    while KeyCA[4] < KeyAlice[4] or KeyCA[5] < KeyAlice[5]:
        KeyCA = creer_clef()
    while KeyBOB[4] < KeyAlice[4] or KeyBOB[5] < KeyAlice[5]:
        KeyBOB = creer_clef()
    Alice = (KeyAlice[0], KeyAlice[1])
    clé_publiqueAlice = KeyAlice[0]
    clé_priveAlice = KeyAlice[1]
    pA = KeyAlice[2]
    qA = KeyAlice[3]

    CA = (KeyCA[0], KeyCA[1])
    clé_publiqueCA = KeyCA[0]
    clé_priveCA = KeyCA[1]
    pCA = KeyCA[2]
    qCA = KeyCA[3]

    BOB = (KeyBOB[0], KeyBOB[1])
    clé_publiqueBOB = KeyBOB[0]
    clé_priveBOB = KeyBOB[1]
    pB = KeyBOB[2]
    qB = KeyBOB[3]

    certificat = creationCertificat(Alice, clé_publiqueCA)
    empreinte = certificat[2]
    message = getCertificat(
        certificat[0], certificat[1], empreinte, clé_publiqueAlice[1], CA)
    messageChiffre = RSA(message, clé_publiqueBOB)
    messageDechiffre = decryRSA(messageChiffre, clé_priveBOB)

    BobVerifEmpreinte = messageDechiffre == message
    if BobVerifEmpreinte == False:
        print("Bob n'a pas pu vérifier l'empreinte !")
        main()

    print("2 nombres probables premiers p et q choisis aléatoirement par Alice", pA, qA)
    print("n = p*q = ", pA*qA)
    print("phi(n)= ", (pA-1)*(qA-1))
    print("clé publique Alice : ", clé_publiqueAlice)
    print("clé privée Alice : ", clé_priveAlice)

    print("2 nombres probables premiers p et q choisis aléatoirement par CA", pCA, qCA)
    print("n = p*q = ", pCA*qCA)
    print("phi(n)= ", (pCA-1)*(qCA-1))
    print("clé publique CA : ", clé_publiqueCA)
    print("clé privée CA : ", clé_priveCA)

    print("ALICE Communique de manière confidentielle avec CA, en chiffrant avec la clé publique de CA :", RSA(
        message, clé_publiqueCA))

    print("CA déchiffre le message avec sa clé privée :",
          decryRSA(message, clé_priveCA))

    print("on verifie le certificat : ", message)
    print("CA : Génére le certificat de la clé publique d'Alice :",
          creationCertificat(CA, clé_publiqueAlice))
    print("Chiffre de la clé publique d'Alice avec la clé privée de CA :",
          RSA(clé_publiqueAlice, clé_priveCA))
    print("BOB : Génére sa clé publique et sa clé privée :", BOB)
    print("Alice chiffre le message avec la clé publique de BOB :", messageChiffre)
    print("Alice envoie le message a BOB et BOB déchiffre avec sa clé privée :", messageDechiffre)
    print("BOB vérifie l'empreinte du message :", BobVerifEmpreinte)


main()