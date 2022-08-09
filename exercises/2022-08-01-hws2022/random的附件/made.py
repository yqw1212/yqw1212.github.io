# from flag import FLAG
import random
from PIL import Image
from hashlib import md5
from Crypto.Util.number import long_to_bytes as n2b

random.seed(793211)


def pbl(bits):
    num = random.getrandbits(bits)
    bins = []
    while num:
        bins.append(num & 1)
        num >>= 1
    while len(bins) != bits:
        bins.append(0)
    return bins


assert len(FLAG) == 28

cat = Image.open('1.png')
cat1 = Image.new('L', cat.size)
cat2 = Image.new('L', cat.size)
cat3 = Image.new('L', cat.size)

x, y = cat.size
bits = x * y
r1, r2 = pbl(bits), pbl(bits)
r3 = FLAG + n2b(random.getrandbits((bits - len(FLAG)) * 8))
r3 = list(r3)
random.shuffle(r3)

for i in range(x):
    for j in range(y):
        pix = cat.getpixel((i, j))
        cat1.putpixel((i, j), pix[0] ^ r1[i * y + j])
        cat2.putpixel((i, j), pix[1] ^ r2[i * y + j])
        cat3.putpixel((i, j), pix[2] ^ r3[i * y + j])

img = Image.new('RGB', cat.size)
img.putdata([(p1, 0, p3) for p1, p3 in zip(cat1.getdata(), cat3.getdata())])
img.save('xx.png')
