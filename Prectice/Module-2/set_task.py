myset=set()

n=int(input("enter no of values:"))

for i in range(n):
    value=input("enter value:")
    myset.add(value)

print("myset:",myset)

print(len(myset))
