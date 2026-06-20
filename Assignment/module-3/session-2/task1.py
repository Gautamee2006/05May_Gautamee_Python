# Create a Python script that opens a file called lyrics.txt and prints the file pointer's current position using tell() before and after reading the first 10 characters.

f=open("lyrics.txt","w+")

f.write("Learning Python is fun.File handling is useful.Practice makes perfect.")
f.seek(0)

print(f.tell())

x=f.read(10)
print(x)

print(f.tell())