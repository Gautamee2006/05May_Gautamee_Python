data=[]

n=int(input("enter number of students:"))

for i in range (n):
    sdata={}

    m=int(input("enetr pair of student data:"))

    for i in range(m):
        key=input("enter key:")
        value=input("enter value:")

        sdata[key]=value

    data.append(sdata)

print(data)

