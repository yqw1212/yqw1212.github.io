flag = ""
data = "rxusoCqxw{yqK`{KZqag{r`i"
for i in data:
    flag += chr(ord(i)^0x14)

print(flag)