# Write a Python program to calculate grades based on percentage using if-else ladder.

sub1=int(input("enter your marks:"))
sub2=int(input("enter your marks:"))
sub3=int(input("enter your marks:"))
sub4=int(input("enter your marks:"))
sub5=int(input("enter your marks:"))

total=sub1+sub2+sub3+sub4+sub5
print("Total of marks:",total)

pr=total/5
print("pr of student")

if sub1>40 and sub2>40 and sub3>40 and sub4>40 and sub5>40:
    if pr>=80:
        print("A")
    elif pr>60:
        print("B")
    elif pr>40:
        print("c")
else:
    print("fail")    

