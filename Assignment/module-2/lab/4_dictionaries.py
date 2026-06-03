# Write a Python program to create a dictionary with 6 key-value pairs.

dict1={"id":"1","name":"gautamee","city":"rajkot","sub":"python","place":"tops","time":"11:30 to 1:00"}

print(dict1)

#Write a Python program to access values using dictionary keys.

print("name:",dict1["name"])
print("city:",dict1["city"])
print("id:",dict1["id"])

# Write a Python program to update a value in a dictionary.
# Write a Python program to update a value at a particular key in a dictionary.

dict1["city"]='surat'
print(dict1)

# Write a Python program to merge two lists into one dictionary using a loop.
#Write a Python program to convert two lists into one dictionary using a for loop.

l1=['id','name','city']
l2=['1','gautamee','rajkot']

student={}

for i in range(len(l1)):
    student[l1[i]] = l2[i]

print("Merged Dictionary:", student)


# Write a Python program to separate keys and values from a dictionary using keys() and values() methods.

#keys = student.keys()
values = student.values()

print("Keys:",dict1.keys())
print("Values:", list(values))


# Write a Python program to count how many times each character appears in a string.

