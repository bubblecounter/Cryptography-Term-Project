import hashlib
import random

#  proof of work function for transactions in TXfile
def PoW(PoWLen, TxFile):
    f = open(TxFile, "r")
    transactions = f.readlines()
    transactions = "".join(transactions)
    while True:
        nonce = str(random.randint(0,2**128-1))  # creates a 128 bit random nonce
        block = transactions + nonce  # add nonce to end of transactions
        hash = hashlib.sha3_256(block.encode('UTF-8')).hexdigest()  # compute the hash value
        if hash[0:PoWLen] == "0" * PoWLen:  # check if first PoWLen elements of has value is zero
            return block