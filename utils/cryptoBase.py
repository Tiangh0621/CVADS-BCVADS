import random
import hashlib
import secrets
import math


def rabin_miller(num):
    # Returns True if num is a prime number.

    s = num - 1
    t = 0
    while s & 1 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s >> 1
        t += 1
    # print(num)
    for _ in range(5): # try to falsify num's primality 5 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v == 1 or v == num - 1:
            continue
        if v != 1: # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def is_prime(num):
    # Return True if num is a prime number. This function does a quicker
    # prime number check before calling rabin_miller().

    if (num < 2) or (num & 1== 0):
        return False # 0, 1, and negative numbers are not prime

    # About 1/3 of the time we can quickly determine if num is not prime
    # by dividing by the first few dozen prime numbers. This is quicker
    # than rabin_miller(), but unlike rabin_miller() is not guaranteed to
    # prove that a number is prime.
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 
        113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 
        257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 
        409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 
        571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 
        733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 
        907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    if num in lowPrimes:
        return True


    return rabin_miller(num)


def generate_large_prime(num_of_bits):
    while True:
        num = secrets.randbelow(pow(2, num_of_bits))
        if is_prime(num):
            return num
def hash_to_prime(x, num_of_bits=128, nonce=0):
    while True:
        num = hash_to_length(x + nonce, num_of_bits)
        # print(num)
        if is_prime(num):
            return num, nonce
        nonce = nonce + 1


def hash_to_length(x, num_of_bits):
    pseudo_random_hex_string = ""
    num_of_blocks = math.ceil(num_of_bits / 256)
    for i in range(0, num_of_blocks):
        pseudo_random_hex_string += hashlib.sha256(str(x + i).encode()).hexdigest()
    if num_of_bits % 256 > 0:
        # bug!!!!!!!!!!!!!!!!!!!!!
        pseudo_random_hex_string = pseudo_random_hex_string[:int((num_of_bits % 256)/4)]  # we do assume divisible by 4
    # print(pseudo_random_hex_string)
    return int(pseudo_random_hex_string, 16)


def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0

def generate_mutual_prime(a, N):
    x = xgcd(a, N)[1]
    if x < 0:
        d = x + N
    else:
        d = x
    return d
        

def generate_squre_root(N):
    a = 997
    ans = a*a%N 
    return ans


def str_to_int(s):
    # 文本转16进制 
    ans = 0
    # print(s)
    for c in s:
        ans *= 256
        ans += int(hex(ord(c)).replace('0x', ''),16)
    return ans
