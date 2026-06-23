#seek() ka use cursor ki position change karne ke liye hota hai.
'''f.seek(offset, from_what)
offset = kitna move karna hai
from_what = kis position se move karna hai'''

'''f = open("demo.txt", "r")

f.seek(3, 0)

print(f.tell())

f.close()'''

f=open("test.txt",'r')

f.seek(5)

print(f.read())

f.close()