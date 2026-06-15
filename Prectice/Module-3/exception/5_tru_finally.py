try:
    a=int(input("enter no of a:"))
    v=int(input("enter no of b:"))
    print("sum is:",a+v)

except Exception as e:
    print(e)

finally:
    print("this is finally block")  