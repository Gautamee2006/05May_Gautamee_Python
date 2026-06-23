'''f=open("test.txt","w")

#count=f.write("hello")  
#count=f.write(100)#error
count=f.write(str(100))
print(count)

f.close()'''

f = open("test.txt", "a")

data = [10, 20, 30]
f.write(str(data))

f.close()