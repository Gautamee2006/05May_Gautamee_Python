set1={'a','b','c','d','e'}

print(set1)

print(len(set1))

if 'b' in set1:
    print("yes...")
else:
    print("no..")



for i in set1:
    print(i)

#-----------------------------
set1.add('gatu')
print(set1)

set1.update('g','h','j')
print(set1)

set1.remove('a')
print(set1)

set1.pop()
print(set1)