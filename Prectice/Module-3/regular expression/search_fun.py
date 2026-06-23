import re

st="This is Python!"

x=re.search("Python",st)
print(x)

if x:
    print("Match Done!")
else:
    print("Error!")