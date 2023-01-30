import opglib

# print(opglib.decode('e.opg'))
f = open('img.opg')
opglib.decode(f)
fp = open("img.png")
print(opglib.encode(fp))