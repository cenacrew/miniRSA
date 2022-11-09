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


def testPrime( n)  :

  if ((puissance(2,n-1,n)==1) and
        (puissance(3,n-1,n)==1) and
        (puissance(5,n-1,n)==1) and
        (puissance(7,n-1,n)==1)and
        (puissance(11,n-1,n)==1) and
        (puissance(13,n-1,n)==1)) :
        return True
  return False

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