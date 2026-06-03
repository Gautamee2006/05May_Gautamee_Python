# Write a Python program to create a list with elements of multiple data types (integers, strings, floats, etc.).

l1=['python','c++',11,8.6,True]

print(l1)

# Write a Python program to access elements at different index positions.
#get the value
'''print(l1[-1])
print(l1[1])
print(l1[2:5])
print(l1[:4])
print(l1[2:])
'''
#change the value
'''l1[1]='java'
print(l1)'''

#==============================================================================================

# Write a Python program to iterate over a list using a for loop.
'''for i in l1:
    print(i)'''

#===============================================================================================

'''if 'gautami' in l1:
    print("yes.....")
else:
    print("no.....")
'''
#===============================================================================================

'''print(len(l1))'''

#===============================================================================================

#Write a Python program to add elements to a list using insert() and append().
'''l1.append("php")
l1.insert(1,"c#")
'''

#Write a Python program to remove elements from a list using pop() and remove().
'''l1.remove("c#")
l1.pop()'''

'''del l1[1]
l1.clear()
del l1
print(l1)
'''

#===============================================================================================

'''newlist=l1.copy()
print(newlist)'''

#==============================================================================================

'''l2=['English','Gujarati','hindi']
print(l2)

l3=l1+l2
print(l3)

l1.extend(l2)
print(l1)'''

#===============================================================================================

l2=[24,5,23,65,46,36]

l2.sort()
print("after sorting:",l2)

l3=sorted(l2)
print(l3)