data=[]

n=int(input("enter total number of dict:"))

for i in range(n):
    dict1={}

    m=int(input("enter pair of dict:"))

    for j in range(m):
        key=input("enter key name:")
        Value=input("enter value name:")
        dict1[key]=Value
    
    data.append(dict1)

print(data)