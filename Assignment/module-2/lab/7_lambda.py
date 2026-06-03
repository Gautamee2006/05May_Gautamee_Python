#  Write a Python program to create a lambda function with one expression.

x=lambda a,b:a+b
print(x(1,2))

# Write a Python program to create a lambda function with two expressions.

x=lambda a,b,y,z:(a+b,y*z)
print(x(2,3,4,5))

print("sum is:",x(12,12,12,12)[0])
