# Simulate a Zomato-style order history: create a file orders.txt with at least 5 lines 
# each line is an order). Write a script that reads and prints each order line-by-line using a loop,
# and after reading each line, prints the file pointer's position using tell().

f=open("orders.txt","r")

print("current position:",f.tell())

'''for i in f:
    print(i)
    x=f.tell()
    print("position",x)'''#if ke sath tell work nahi karta

while True:
    i=f.readline()
    if i=="":
        break
    print(i.strip())
    print("position:",f.tell())

f.close()

'''optput:
current position: 0
Pizza
position: 7 (5 char or ek line space ginega or ek dusri line me jata hai es liye \n ke sath\r bbhi hota hai)
Vada pau
position: 17
Pau bhaji
position: 28
Dosa
position: 34
Sandwich
position: 42'''