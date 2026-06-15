import os
from datetime import datetime

os.chdir("file handling")

students=int(input("enter numer of student:"))

file=open("students_data.txt","w")

for i in range(students):
    time=datetime.now()
    id=input("enter s.id:")
    name=input("enter s.name:")
    city=input("enter s.city:")
    
    file.write(f'time:{time}\n')
    file.write(f'id:{id}\n')
    file.write(f'name:{name}\n')
    file.write(f'city:{city}\n')
    file.write("-----------------------------------------------------\n")