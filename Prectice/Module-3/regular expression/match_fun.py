import re

st="This is Python!"

x=re.match("This",st)#frist word will be considered
print(x)

if x:
    print("Match Done!")
else:
    print("Error!")