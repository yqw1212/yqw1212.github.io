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



FLAG=b"flag{!@#1234567890abcdefghi}"
assert len(FLAG) == 28
fake_cat = Image.open('xx.png')
# cat1 = Image.new('L', cat.size)
# cat2 = Image.new('L', cat.size)
# cat3 = Image.new('L', cat.size)
cat = Image.open('1.png')
x, y = cat.size
bits = x * y
print(bits)
r1, r2 = pbl(bits), pbl(bits)
r3 = FLAG + n2b(random.getrandbits((bits - len(FLAG)) * 8))
r3 = list(r3)
random.shuffle(r3)
n=0
tmp=0
res=[]
ans=[]
for i in range(x):
    for j in range(y):
        fake_pix = fake_cat.getpixel((i, j))
        fp1=fake_pix[0]
        fp3=fake_pix[2]
        pix = cat.getpixel((i,j))
        p1=pix[0]
        p3=pix[2]
        if(p3^r3[i * y + j]!=fp3):
            ans.append(chr(r3[i * y + j]))
            while(p3^tmp!=fp3 and tmp<256):
                tmp+=1
            
            if(tmp==256):
                print("error")
            else:
                print(chr(tmp))
                res.append(chr(tmp))
                print(i,j)
                n+=1
                tmp=0
print(n)
print(ans)
print(res)
        # cat1.putpixel((i, j), pix[0] ^ r1[i * y + j])
        # cat2.putpixel((i, j), pix[1] ^ r2[i * y + j])
        # cat3.putpixel((i, j), pix[2] ^ r3[i * y + j])
        # print(pix)

# img = Image.new('RGB', cat.size)
# img.putdata([(p1, 0, p3) for p1, p3 in zip(cat1.getdata(), cat3.getdata())])
# img.save('xx.png')

# lovely_cat_with_random