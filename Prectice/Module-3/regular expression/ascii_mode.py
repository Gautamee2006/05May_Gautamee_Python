import re

st="This is Python!2323234"

#x=re.findall("\w",st) # return only 0-9,a-z,A-Z
#x=re.findall("\W",st) #return only special char or space
#x=re.findall("\d",st) # return only 0-9
#x=re.findall("\D",st) # return only special char ,space,A-Z,a-z
#x=re.findall("\s",st) # return only space
#x=re.findall("\S",st) # not allow space
#x=re.findall(r"\bThis",st)
#x=re.findall("\B23",st)
#x=re.findall("\AThis",st)
x=re.findall("22\Z",st)
print(x)
