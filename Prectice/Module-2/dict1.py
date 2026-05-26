data={'id':1,'name':'gautamee','city':'rajkot'}

#get tha value
print(data)
print(data["name"])
print(data.get("city"))

#---------------------------------------------
print(data.keys())
print(data.values())

#---------------------------------------------
print(len(data))

#---------------------------------------------
if 'name' in data:
    print("yess...")
else:
    print("no..")


if 'gautamee' in data.values():
    print("yess...")
else:
    print("no..")


for i in data:
    print(i)


for i in data.values():
    print(i)


for i in data.items():
    print(i)


for i,j in data.items():
    print(i,j)
    print(f"ket{i} and value{j}")

#---------------------------------------------
data["id"]=2     #upadte
print(data)

data['sub']='python'  #vlaue
print(data)

data.pop('city')
print(data)

data.popitem()
print(data)

data.clear()
print(data)

del data
print(data)

d1=data.copy
print(d1)