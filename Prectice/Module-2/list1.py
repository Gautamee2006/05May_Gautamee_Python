city=[]

n=int(input("How many city do you want to enter?"))

for i in range(n):
    name=input("enter city name:")
    city.append(name)

print("list of city:",city)