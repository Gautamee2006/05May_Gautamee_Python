import re

st="This is Python!"

x=re.findall("is",st)#give the list
print(x)

if x:
    print("Match Done!")
else:
    print("Error!")