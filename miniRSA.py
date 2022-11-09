def puissance (a,e,n):
    if e == 0:
        return 1
    elif e == 1:
        return a
    else:
        return (a**e)%n


def test_premier(n):
    for i in range(2,n):
        if n%i == 0:
            return False
    return True

def pgcd(a,b):
    if b == 0:
        return a
    else:
        return pgcd(b,a%b)

def bezout(a,b):
    if b == 0:
        return (1,0)
    else:
        (u,v) = bezout(b,a%b)
        return (v,u-(a//b)*v)