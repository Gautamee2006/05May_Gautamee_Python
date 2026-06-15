import os

os.chdir('file handling')
file=open('temp.txt','r')

#print(file.read())
print(file.readline())
#print(file.readlines())

#print(file.readlines()[1])