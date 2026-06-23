import re

mystr="This is Python!454"

x=re.findall('^This',mystr)
#x=re.findall('^[A-Z]',mystr)
#x=re.findall("54$",mystr)
print(x)