'''
A 
A B 
A B C 
A B C D 
A B C D E '''
for i in range(5):
    for j in range(i + 1):
        print(chr(65 + j), end=" ")
    print()