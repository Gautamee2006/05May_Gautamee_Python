s1=int(input("enter marks of s1:"))
s2=int(input("enter marks of s2:"))
s3=int(input("enter marks of s3:"))
s4=int(input("enter marks of s4:"))

total=s1+s2+s3+s4

pr=total/4

print("total of marks:",total)
print("pr of student:",pr)

if s1>=40 and s2>=40 and s3>=40 and s4>=40:
    if(pr>=90):
        print("A")
    elif(pr>=70):
        print("B")
    elif(pr>=50):
        print("C")
else:
    print("fail")
