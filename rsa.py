# -*- coding: utf-8 -*-
import random
import math

from random import randrange

class RSA :
    n = 0
    d = 0
    e = 0
    
    def GenerateKeys(self):
        keySize = 17
        
        p = RSA.GeneratePrimes(keySize)
        
        q = RSA.GeneratePrimes(keySize)
        while(p == q):
            q = RSA.GeneratePrimes(keySize)
        
        n = p*q
       
        fi = (p - 1)*(q-1)
       
        e = random.randrange(1, fi)
        
        #print(e)
        d = RSA.multiplicativeInverse(e,fi)
        
        self.n = n
        self.e = e
        self.d = d
        
    def GeneratePrimes(k):
         r = 100*(math.log(k,2)+1)
         while r>0:
            n = random.randrange(10**(k-1),10**(k))
            r -= 1
            if RSA.isPrime(n) == True:
                return n
            
    def multiplicativeInverse(a, b):
        x = 0
        y = 1
        lx = 1
        ly = 0
        oa = a  # Remember original a/b to remove
        ob = b  # negative values from return results
        while b != 0:
            q = a // b
            (a, b) = (b, a % b)
            (x, lx) = ((lx - (q * x)), x)
            (y, ly) = ((ly - (q * y)), y)
        if lx < 0:
            lx += ob 
        if ly < 0:
            ly += oa  
        return lx

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = RSA.egcd(b%a,a)
        return (g, x - (b//a) * y, y)
    
    def rabinMiller(n, k=10):
        def check(a, s, d, n):
                x = pow(a, d, n)
                if x == 1:
                        return True
                for i in range(1, s - 1):
                        if x == n - 1:
                                return True
                        x = pow(x, 2, n)
                return x == n - 1
    
        s = 0
        d = n - 1
    
        while d % 2 == 0:
                d >>= 1
                s += 1
    
        for i in range(1, k):
                a = randrange(2, n - 1)
                if not check(a, s, d, n):
                        return False
        return True

    def isPrime(n):
         lowPrimes =   [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                       ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                       ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                       ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                       ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                       ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                       ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                       ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                       ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                       ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
         if (n >= 3):
             if (n&1 != 0):
                 for p in lowPrimes:
                     if (n == p):
                        return True
                     if (n % p == 0):
                         return False
                 return RSA.rabinMiller(n)
         return False
    def podepsat(self,string):
        cipher = [str(pow(ord(char), self.d, self.n)) for char in string]
        return " ".join(cipher);
    def desifrovat(self,string):
        plain = [chr(pow(int(char) ,self.e, self.n)) for char in string]
        return "".join(plain)
        
         
        self.Output.setText("".join(plain))
    def __init__(self):
        self.GenerateKeys();
        