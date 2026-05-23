#Write a Python program to find greater and less than a number using if...else

a=int(input("enter any number:"))
b=int(input("enter any number:"))

if a>b:
    print(a,"grater than",b)
elif a<b:
    print(a,"less than",b)
else:
    print("both are equal")