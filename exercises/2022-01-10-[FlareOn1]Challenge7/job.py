#!/usr/bin/env python

from itertools import product
import array
import string

keys = [['the final countdown','oh happy dayz'],
['UNACCEPTABLE!','omglob'],
["you're so good","you're so bad"],
["\x66","\x01"],
["I'm gonna sandbox your face","Sandboxes are fun to play in"],
["Such fire. Much burn. Wow.","I can haz decode?"],
["Feel the sting of the Monarch!","\x09\x00\x00\x01"],
["\x21\x20\x35\x30\x20\x31\x33\x33\x37"],
["MATH IS HARD","LETS GO SHOPPING"],
["LETS GO MATH","SHOPPING IS HARD"],
["\x01\x02\x03\x05\x00\x78\x30\x38\x0D"],
["backdoge.exe"],
["192.203.230.10"],
["jackRAT"]]

encrypted_file = bytearray(open('encrypted.bin', 'rb').read())

def xor(data, key):
       l = len(key)
       return bytearray((
       (data[i] ^ key[i % l]) for i in range(0,len(data))
       ))

for x in product(*keys):
  version = encrypted_file
  for y in x:
    version = xor(version,array.array('B', y))
  if (version.find("DOS mode") != -1):
    open('gratz.exe', 'wb').write(version)
    print(x)
    quit()