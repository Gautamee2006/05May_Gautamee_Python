name=['riya','gautamee','janvi','priya','hinali']

print(name)

print(name[0])

print(name[3])

print(name[2:5])

print(len(name))

#name[2]='bhumi'
#print(name)

for i in name:
    print(i)

if 'gautamee' in name:
    print("yes....")
else:
    print("no....")

#name.append('bhumi')
#print(name)

#name.insert(0,'gatu')
#print(name)

#name.reverse()
#print(name)

newname=name.copy()
print(newname)

n1=[]
name.extend(newname)