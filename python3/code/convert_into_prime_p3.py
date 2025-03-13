import math
import random
import sys
from PIL import Image

sys.set_int_max_str_digits(0)

def ipow(a, b, n):
    A = a = a % n
    yield A
    t = 1
    while t <= b:
        t <<= 1
    
    t >>= 2
    while t:
        A = (A * A) % n
        if t & b:
            A = (A * a) % n
        yield A
        t >>= 1

def MillerRabinTest(test, possible):
    return 1 not in ipow(test, possible - 1, possible)

small_primes = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
               47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)

def test_prime(p, k=None):
    if k is None:
        bits = math.log(p, 2) + 1
        k = int(2 * bits)
    
    for i in small_primes:
        if p % i == 0:
            return False
    
    for i in range(k):
        if i > 20:
            print("These are likely to be prime, test", i, "of", k)
        test = random.randrange(2, p) | 1
        if MillerRabinTest(test, p):
            return False
    return True

if len(sys.argv) <= 3:
    print("Missing arguments, to use the script:", sys.argv[0], "[Image path] {width} {height}")
    sys.exit()

basefn = sys.argv[1]
img = Image.open(basefn)
W, H = int(sys.argv[2]), int(sys.argv[3])

def convert_image(img, W, H):
    img = img.resize((W, H), Image.LANCZOS)
    img = img.convert('L')
    avr = sum(img.getdata()) / (W * H)
    bw = img.point(lambda x: 0 if x < avr else 255, '1')
    ps = "".join("1" if c > 128 else "8" for c in bw.getdata())
    ps = ps[:-1] + "1"
    
    print("The image will look like this (warning: this number is not prime yet!).")
    for i in range(H):
        print(ps[i * W: i * W + W])
    return ps

def change(ps):
    ran_pos = random.randrange(len(ps))
    c = ps[ran_pos]
    n = "7" if c == "1" else random.choice(["0", "9", "6", "4", "5", "2", "3"])
    return ps[:ran_pos] + n + ps[ran_pos + 1:]

def find_prime(ps):
    if test_prime(int(ps), 50):
        return ps
    
    i = 1
    print("Finding Prime")
    while True:
        sys.stdout.write('.')
        sys.stdout.flush()
        if i % 50 == 0:
            print(" ")
        i += 1
        P = change(ps)
        if test_prime(int(P), 50):
            return P

if __name__ == "__main__":
    
    number_image = convert_image(img, W, H)
    prime_image = find_prime(number_image)
    print("PRIME FOUND!")
    for i in range(H):
        print(prime_image[i * W: i * W + W])