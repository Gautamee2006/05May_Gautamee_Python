import re

st="This is Python!123"

#x=re.findall("[A-Z]",st)
#x=re.findall("[a-z]",st)
#x=re.findall("[0-9]",st)
x=re.findall("[A-Z0-9a-z]",st)
print(x)