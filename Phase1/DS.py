#Written by A.Furkan Okuyucu
#CS 411 Project Phase 1

import random
import pyprimes
import os.path
import hashlib

# function given in homework
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

# function given in homework
def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

# check if file for public parameters exist
# if file exist read q,p,g respectively and returns
# else generates q , p , q as defined in chapter 10 slide 15
# writes generated q,p,g to pubparams.txt and returns them respectively
def GenerateOrRead(filename):
    if os.path.isfile(filename):  # check if pubparams exist.
        inputfile = open(filename, 'r')
        q = int(inputfile.readline())
        p = int(inputfile.readline())
        g = int(inputfile.readline())
    else:
        small = 1 << 224
        big = 1 << 2048
        foundq = False
        foundp = False
        foundg = False
        while not foundq:
            q = random.randint(0, small - 1)  # generates 224 bit number
            if pyprimes.isprime(q):
                foundq = True

        while not foundp:
            p = q * random.randint(0, int(big // small)) + 1  # generates 2048 bit p (q % p-1 = 0 )
            if pyprimes.isprime(p):
                foundp = True

        while not foundg:
            alpha = random.randint(0, p - 1)  # alpha is a random integer in mod p
            g = pow(alpha, int((p - 1) // q), p)
            if g != 1:
                foundg = True

        outputfile = open('pubparams.txt', 'w')
        outputfile.write(str(q) + "\n")
        outputfile.write(str(p) + "\n")
        outputfile.write(str(g) + "\n")
        outputfile.close()

    return q, p, g


# Generates key pair (a,b) as defined in chapter 10 slide 15
def KeyGen(q, p, g):
    a = random.randint(1, q - 1)
    beta = pow(g, a, p)

    return a, beta


def random_string(size):
    message = ''
    possibleChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for i in range(size):
        a = random.choice(possibleChars)
        message.join(a)
    return message

# it generates signature
def SignGen(message, q, p, g, alpha):
    k = random.randint(0, q - 1)
    r = pow(g, k, p)
    m = message.decode('UTF-8')
    m =  m + str(r)
    m = m.encode('UTF-8')
    h = int(hashlib.sha3_256(m).hexdigest(),16)
    s = (alpha * h + k) % q

    return s, h

# it verifies the signature
def SignVer (message, s, h, q, p, g, beta):
    betainverse = modinv(beta,p)
    v = (pow(g,s,p)*pow(betainverse,h,p))% p
    m = message.decode('UTF-8')
    m = m + str(v)
    m = m.encode('UTF-8')
    hp = int(hashlib.sha3_256(m).hexdigest(),16)
    h = h % q
    hp = hp % q
    if h == hp:
        return 0
    else:
        return -1