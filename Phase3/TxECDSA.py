import random
import hashlib
from ecpy.curves import Curve,Point
from ecpy.keys import ECPublicKey, ECPrivateKey
from ecpy.ecdsa import ECDSA
from ecpy.formatters import decode_sig, encode_sig

def gen_random_tx(curve):
    serial = random.randint(0, 2 ** 128 - 1)  # creates 128 bit random serial number
    n = curve.order
    P = curve.generator
    sA = random.randint(0, n)
    sk = ECPrivateKey(sA, curve)
    QA = sA * P
    pk = ECPublicKey(QA)

    sB = random.randint(0, n)
    skB = ECPrivateKey(sB, curve)
    QB = sB * P
    pkB = ECPublicKey(QB)

    amount = random.randint(1, 1000000)  # create a random int for amount

    transaction = "**** Bitcoin transaction ****\n"
    transaction += "Serial number: " + str(serial) + "\n"
    transaction += "Payer public key - x: " + str(QA.x)+"\n"
    transaction += "Payer public key - y: " + str(QA.y) + "\n"
    transaction += "Payee public key - x: " + str(QB.x) + "\n"
    transaction += "Payee public key - y: " + str(QB.y) + "\n"
    transaction += "Amount: " + str(amount) + "\n"

    signer = ECDSA()

    message = transaction
    message = message.encode('UTF-8')
    sig = signer.sign(message, sk)

    (r, s) = decode_sig(sig)

    transaction += "Signature (r): " + str(r) + "\n"
    transaction += "Signature (s): " + str(s) + "\n"
    return transaction