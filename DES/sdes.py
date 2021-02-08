P10 = [3,5,2,7,4,10,1,9,8,6]
P8 = [6,3,7,4,8,5,10,9]
IP = [2,6,3,1,4,8,5,7]
EP = [4,1,2,3,2,3,4,1]
S = [[[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]],
     [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]]
P4 = [2,4,3,1]
InP = [4,1,3,5,7,2,8,6]

def permute(vec,pbox):
    return [ vec[pbox[i]-1] for i in range(len(pbox)) ]

def leftshift(vec,offset):
    return [ vec[(i+offset)%len(vec)] for i in range(len(vec)) ]

def generate_keys(key):
    keys = []
    k = permute(key,P10)
    kl = k[:len(k)/2]
    kr = k[len(k)/2:]

    kl_shift1 = leftshift(kl,1)
    kr_shift1 = leftshift(kr,1)

    kl_shift2 = leftshift(kl_shift1,2)
    kr_shift2 = leftshift(kr_shift1,2)

    k1_before_P8 = kl_shift1 + kr_shift1
    k2_before_P8 = kl_shift2 + kr_shift2

    k1 = permute(k1_before_P8,P8)
    k2 = permute(k2_before_P8,P8)

    keys.append(k1)
    keys.append(k2)

    return keys

def XOR(v1,v2):
    v3 = []
    for i in range(len(v1)):
        if v1[i] == v2[i]:
            v3.append(0)
        else:
            v3.append(1)
    return v3

def char2bool(val):
    tmp = []
    for c in range(0,2):
        tmp.append(val%2)
        val = (val - (val%2))/2
    return tmp[::-1]

def sbox(vec,s):
    row = vec[0]*2 + vec[3]
    col = vec[1]*2 + vec[2]
    return char2bool(s[row][col])

def encrypt(plain_text,keys,switch):
    msg = permute(plain_text,IP)
    msgL = [msg[:len(msg)/2]]
    msgR = [msg[len(msg)/2:]]

    for i in range(2):
        res = permute(msgR[i],EP)
        if switch == 1:
            res = XOR(res,keys[i])
        else:
            res = XOR(res,keys[len(keys)-1-i])
        resL = res[:len(res)/2]
        resR = res[len(res)/2:]
        s0 = sbox(resL,S[0])
        s1 = sbox(resR,S[1])
        res = s0 + s1
        res = permute(res,P4)
        res = XOR(res,msgL[i])
        msgR.append(res)
        msgL.append(msgR[i])

    msg = msgR[2] + msgL[2] #reswap
    return permute(msg,InP)

def main():
    #plain_text = [0,1,1,1,0,0,1,0]
    #key = [1,0,1,0,0,0,0,0,1,0]
    plain_text = []
    key = []
    print ("Input plaintext (8 digits): ")
    for x in range(0,8):
    	ip = input()
    	plain_text.append(ip)
    print ("Input keys (10 digits): ")
    for x in range(0,10):
    	ip = input()
    	key.append(ip)
    keys = generate_keys(key)
    #plain_text = [0,1,1,0,1,1,0,1]
    #keys = [[1,0,1,0,0,1,0,0],[0,1,0,0,0,0,1,1]]
    print("Plain text: ",plain_text)
    cipher_text = encrypt(plain_text,keys,1)
    print("Cipher text: ",cipher_text)
    decrypted_text = encrypt(cipher_text,keys,0)
    print("Decrypted text: ",decrypted_text)

if __name__ == '__main__':
    main()
