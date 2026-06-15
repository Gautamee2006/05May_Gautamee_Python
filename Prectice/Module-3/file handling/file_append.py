import os
os.chdir("file handling")
file=open("temp.txt",'a')

id=input("enter ans id:")
name=input("enter a name:")

file.write(f'{name}\n{id}')