from Crypto.Cipher import AES

def AESdecrypt(data, key, iv):
    aes1 = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes1.decrypt(data)
    return decrypted

aeskey = "37eaae0141f1a3adf8a1dee655853766".decode("hex")
iv = "a5efdbd57b84ca88"
data = "db6427960a6622ffac27ef5437acf1459a592d1a96b73e75490c8badb0ed294c1e9232213e63461dd2d9f6d327e51641".decode("hex")
print(AESdecrypt(data, aeskey, iv))
