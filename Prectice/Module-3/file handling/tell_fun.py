#f.tell() file me current cursor position batata hai.
f=open("test.txt","r")  
print(f.tell())
f.read(5)
print(f.tell())
f.close()