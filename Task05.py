import random

# Hamming(15,11): creates blocks of 11 bits of data and 4 parity bits (minimum distance 3, can fix 1 error)

def hammingEncode(block11): #Receives 11 bits to prepare a 15 block
    # 1. Preparation of data bits into 16-bit array (15, 0 not used)
    dataBits = [0] + block11               # pad so data starts at index 1
    bits = [0]*16                          # 1..15 used, this is the 15 bit block to be prepared
    dataPos = [3,5,6,7,9,10,11,12,13,14,15] # The positions for the data bits are non-powers of 2

    for i,j in enumerate(dataPos,1): # enumerate to use an iterator of dataPos with index i starting in 1 and p having the actual values of dataPos.
        bits[j] = dataBits[i] # assigns the values received in block11 to the proper positions in bits

    # 2. Redundancy (give proper value to parity bits)
    for p in [1,2,4,8]: # for in parity bits' positions
        parity = 0
        for i in range(1,16): #[1,16); 1 to 15
            if i & p: # Binary AND; true for all in the range the given p checks. Each p being 0001,0010,0100,1000, if 
                parity ^= bits[i] # Using XOR, the parity bit is changed to 0 or 1 for each 1 in the range of the parity.
        bits[p] = parity # Once the parity value is properly calculated, it's stored in its position
    return bits[1:] # Returns the slice of bits without the position 0 (unused); skips bits(0)

def hammingDecode(block15): #Receives a properly prepared 15 bit block
    syndrome = 0  # Initializes the var syndrome (position of error if there is)
    for p in [1,2,4,8]: # Analogous to the Encoding, p being each parity bit position
        parity = 0  # Value of parity in position p
        for i in range(1,16): # Goes through the entire block, 1 to 15
            if i & p: # Checks if in range
                parity ^= block15[i-1] # XORs all bits of each parity group
        if parity: # Checks parity (it should be 0 if no error happened)
            syndrome += p # if parity is different than 0, we add the value to syndrome
    if syndrome:
        block15[syndrome-1] ^= 1 # if syndrome isn't 0 (there's been an error) we change the value of the position of the syndrome to correct
    # Once error has been found, returns only the data bits
    dataPos = [3,5,6,7,9,10,11,12,13,14,15]
    return [block15[i-1] for i in dataPos]

# Main code
sentMessage = "Contraseña"
print("String original: "+sentMessage)
bitString = "".join(f"{ord(c):08b}" for c in sentMessage)
print("bitString: "+bitString)
# split into 11-bit blocks
blocks11 = [list(map(int, bitString[i:i+11])) for i in range(0, len(bitString), 11)] # Returns a list of lists(each being a block of 11 bits). map applies the int() function to all values of bitString and returns the map object, with each bit as an Integer and element of the map.
if len(blocks11[-1]) < 11: # Checks the length of the last block to see if it's less than 11
    blocks11[-1] += [0]*(11 - len(blocks11[-1]))  # pad with zeros the last one so it's of 11 bits as well

encodedBlocks = [hammingEncode(block) for block in blocks11] # Apply the function hammingEncode to each block of 11 bits

# introduce one random bit error in each block
for block in encodedBlocks:
    block[random.randrange(15)] ^= 1 #random.randrange(15) gives a random value between 0 and 14 and with XOR 1 flip the value of the bit

decodedBlocks = [hammingDecode(block) for block in encodedBlocks] # Function hammingDecode for each block of 15 in encoded
decodedBitString = "".join("".join(map(str, block)) for block in decodedBlocks) # "".join to have a String, map(str) to convert to string
decodedBitString = decodedBitString[:len(bitString)]  # remove padding, not really needed tho

receivedMessage = "".join(chr(int(decodedBitString[i:i+8],2)) for i in range(0,len(decodedBitString),8))
print(receivedMessage)
