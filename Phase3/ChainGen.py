import hashlib
import random

def AddBlock2Chain(PoWLen, PrevBlock, block_candidate):
    if(PrevBlock == 0):
        hashPrev ="b'0'"
    else:
        hashPrev = hashlib.sha3_256(PrevBlock.encode('UTF-8')).hexdigest()
    block_candidate += "Previous Hash: " + str(hashPrev) + "\n"
    block_candidate += "Nonce: "
    while True:
        nonce = str(random.randint(0,2**128-1))  # creates a 128 bit random nonce
        block = block_candidate + nonce  # add nonce to end of transactions
        hash = hashlib.sha3_256(block.encode('UTF-8')).hexdigest()  # compute the hash value
        if hash[0:PoWLen] == "0" * PoWLen:  # check if first PoWLen elements of has value is zero
            return block_candidate + nonce
