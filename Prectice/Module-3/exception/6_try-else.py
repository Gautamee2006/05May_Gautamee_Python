try:
    a=int(input("enter no of a:"))
    v=int(input("enter no of b:"))
    print("sum is:",a+v)

except Exception as e:
    print(e)

else:
    print("this is else block")