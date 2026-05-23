# Write a Python program to check if a person is eligible to donate blood using a nested if.


age = int(input("Enter your age: "))
weight = int(input("Enter your weight: "))

if age >= 18:
    if weight >= 50:
        print("eligible to donate blood.")
    else:
        print("Not eligible because weight is less than 50 kg.")
else:
    print("not eligible because age is less than 18.")