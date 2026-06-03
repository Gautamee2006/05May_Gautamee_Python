#  Create a mini-project where students combine conditional statements, loops, and functions to create a basic Python application, such as a simple calculator or a grade management system.


#simple calculator

def addition(a,b):
    print(a,'+',b,'=',a+b)

def subtraction(a,b):
    print(a,'-',b,'=',a-b)

def multiplication(a,b):
    print(a,'*',b,'=',a*b)

def division(a,b):
    if b==0:
        print("division is not possible")
    else:
        print(a,'/',b,'=',a/b)
    
def modulus(a,b):
    print(a,'%',b,'=',a%b)

def power(a,b):
    print(a,'**',b,'=',a**b)

def floor_division(a,b):
    print(a,'//',b,'=',a//b)


for i in range(4):
    print()
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multipliction")
    print("4. Division")
    print("5. Modulus")
    print("6. Power")
    print("7. Floor Division")
    print("8. Exit")
    print()

    choice = int(input("enter your choice: "))

    if choice==8:
        print("End.....")
        break
    
    if choice<1 or choice>8:
        print("invalid choise...")
        continue

    n1=int(input("enter value of a:"))
    n2=int(input("enter value of b:"))

    if choice==1:
        addition(n1,n2)

    elif choice==2:
        subtraction(n1,n2)

    elif choice==3:
        multiplication(n1,n2)

    elif choice==4:
        division(n1,n2)
        
    elif choice==5:
        modulus(n1,n2)

    elif choice==6:
        power(n1,n2)

    elif choice==7:
        floor_division(n1,n2)
