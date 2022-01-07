# import os

# files = os.listdir("./FLEGGO")
# for filename in files:
#      filename = "./FLEGGO/" + filename
#      with open(filename,"rb") as f:
#           f=f.read()[0x2ab0:0x2ad0]
#      f=f.split(b'\x00')
#      print("\"",end="")
#      for i in f:
#           if i == b'':
#                break
#           print(chr(int().from_bytes(i, byteorder='big', signed=True)), end="")
#      print("\"")

# key=[b"ZImIT7DyCMOeF6",
# b"PylRCpDK",
# b"UvCG4jaaIc4315",
# b"uVmH96JGdPkEBfd",
# b"3nEiXqMnXG",
# b"Q9WdIAGjUKdNxr6",
# b"UkuAJxmt8",
# b"b1VRfMTNPu",
# b"qNb6tr7n",
# b"KSL8EAnlIZin1gG",
# b"uLKEIRAEn",
# b"7kcuVMWeIBFGWfJ",
# b"NcMkqwelbRu",
# b"yu7hNshnpM4Vy",
# b"5xj9HmHyhF",
# b"ZYNGeumv6QuI7",
# b"dRnTVwZPjf0U",
# b"dPVLAQ8LwmhH",
# b"J1kj42jZsC9",
# b"rXZE7pDx3",
# b"eoneTNuryZ3eF",
# b"jZAorSlICuQa0g8",
# b"hqpNm7VJL",
# b"45psrewIRS",
# b"2LUmPSYdxDcil",
# b"aGUwVeVZ2c19mgE",
# b"goTZP4go",
# b"9aIZjTerf0",
# b"jZRmFmeIchneGS",
# b"Z8VCO7XbKUk",
# b"14bm9pHvbufOA",
# b"9eDMpbMSEeZ",
# b"auDB6HtMv",
# b"C446Zdun",
# b"nLSGJ2BdwC",
# b"0d7qdvEhYGc",
# b"5O2godXTZePdWZd",
# b"ohj5W6Goli",
# b"4z0gAyKdk",
# b"r6ZWNWeFadW",
# b"dEDDxJaxc1R",
# b"HQG0By9q",
# b"0rhvT5GX",
# b"Fs3Ogu6W3qk59kZ",
# b"8V9AzigUcb2J",
# b"gNbeYAjn",
# b"8Etmc0DAF8Qv",
# b"XgkvZJKe"]

# import os
# import subprocess

# files = os.listdir("./FLEGGO")
# i=0
# for filename in files:
#     filename = "./FLEGGO/" + filename
#     p = subprocess.Popen([filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     p.stdin.write(key[i])
#     p.stdin.close()
#     i+=1
#     out=p.stdout.read()
#     p.stdout.close()
#     print(out)

flag = [
b'What is the password?\r\nEverything is awesome!\r\n65141174.png => w\r\n',
b'What is the password?\r\nEverything is awesome!\r\n85934406.png => m\r\n',
b'What is the password?\r\nEverything is awesome!\r\n67782682.png => m\r\n',
b'What is the password?\r\nEverything is awesome!\r\n75072258.png => r\r\n',
b'What is the password?\r\nEverything is awesome!\r\n16544936.png => e\r\n',
b'What is the password?\r\nEverything is awesome!\r\n67322218.png => _\r\n',
b'What is the password?\r\nEverything is awesome!\r\n58770751.png => o\r\n',
b'What is the password?\r\nEverything is awesome!\r\n64915798.png => 3\r\n',
b'What is the password?\r\nEverything is awesome!\r\n88763595.png => e\r\n',
b'What is the password?\r\nEverything is awesome!\r\n18376743.png => _\r\n',
b'What is the password?\r\nEverything is awesome!\r\n36870498.png => m\r\n',
b'What is the password?\r\nEverything is awesome!\r\n72501159.png => c\r\n',
b'What is the password?\r\nEverything is awesome!\r\n47619326.png => p\r\n',
b'What is the password?\r\nEverything is awesome!\r\n70037217.png => m\r\n',
b'What is the password?\r\nEverything is awesome!\r\n18309310.png => @\r\n',
b'What is the password?\r\nEverything is awesome!\r\n15566524.png => e\r\n',
b'What is the password?\r\nEverything is awesome!\r\n82100368.png => m\r\n',
b'What is the password?\r\nEverything is awesome!\r\n60075496.png => s\r\n',
b'What is the password?\r\nEverything is awesome!\r\n71290032.png => a\r\n',
b'What is the password?\r\nEverything is awesome!\r\n33718379.png => .\r\n',
b'What is the password?\r\nEverything is awesome!\r\n42255131.png => t\r\n',
b'What is the password?\r\nEverything is awesome!\r\n16295588.png => a\r\n',
b'What is the password?\r\nEverything is awesome!\r\n61333226.png => f\r\n',
b'What is the password?\r\nEverything is awesome!\r\n13147895.png => w\r\n',
b'What is the password?\r\nEverything is awesome!\r\n16785906.png => 4\r\n',
b'What is the password?\r\nEverything is awesome!\r\n80333569.png => o\r\n',
b'What is the password?\r\nEverything is awesome!\r\n37723511.png => n\r\n',
b'What is the password?\r\nEverything is awesome!\r\n44958449.png => _\r\n',
b'What is the password?\r\nEverything is awesome!\r\n30171375.png => s\r\n',
b'What is the password?\r\nEverything is awesome!\r\n72263993.png => h\r\n',
b'What is the password?\r\nEverything is awesome!\r\n82236857.png => e\r\n',
b'What is the password?\r\nEverything is awesome!\r\n33098947.png => _\r\n',
b'What is the password?\r\nEverything is awesome!\r\n33662866.png => r\r\n',
b'What is the password?\r\nEverything is awesome!\r\n47893007.png => _\r\n',
b'What is the password?\r\nEverything is awesome!\r\n61006829.png => l\r\n',
b'What is the password?\r\nEverything is awesome!\r\n89295012.png => 0\r\n',
b'What is the password?\r\nEverything is awesome!\r\n87730986.png => 0\r\n',
b'What is the password?\r\nEverything is awesome!\r\n65626704.png => 3\r\n',
b'What is the password?\r\nEverything is awesome!\r\n72562746.png => -\r\n',
b'What is the password?\r\nEverything is awesome!\r\n36494753.png => 0\r\n',
b'What is the password?\r\nEverything is awesome!\r\n79545849.png => s\r\n',
b'What is the password?\r\nEverything is awesome!\r\n63223880.png => a\r\n',
b'What is the password?\r\nEverything is awesome!\r\n51227743.png => a\r\n',
b'What is the password?\r\nEverything is awesome!\r\n73903128.png => u\r\n',
b'What is the password?\r\nEverything is awesome!\r\n52817899.png => n\r\n',
b'What is the password?\r\nEverything is awesome!\r\n19343964.png => o\r\n',
b'What is the password?\r\nEverything is awesome!\r\n12268605.png => s\r\n',
b'What is the password?\r\nEverything is awesome!\r\n47202222.png => n\r\n']
# f = b""
# for i in flag:
#     f += i[-3:-2]
# print(str(f))

dic = {}
for i in flag:
    dic[str(i[-19:-11], encoding="utf-8")] = str(i[-3:-2], encoding="utf-8")
print(dic)
result = [0 for i in range(49)]
order = [33,23,41,6,24,16,36,21,43,9,
         13,40,45,10,48,17,14,5,20,30,
         29,39,44,47,25,38,37,22,4,7,
         12,18,1,11,19,15,46,42,34,3,
         32,2,27,8,35,26,28,31]
keys = sorted(dic.keys())
for i in range(48):
    result[order[i]] = dic[keys[i]]
print(''.join(str(i) for i in result))