# Simulate a Flipkart order summary calculator that takes price and quantity as 
# input and calculates the total. Use try-except to handle ValueError if the user enters
# a non-numeric value, and display an error message.

try:
    price=float(input("enter the price:"))
    quantity=int(input("enter the quantity of products:"))

    total=price*quantity
    print("total of:",total)
except ValueError:
    print("Invalid!! please enter numeric value")