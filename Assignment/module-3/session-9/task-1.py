'''Write a Python script using the re.match() function to check if a user's inputted email 
address starts with a lowercase letter and contains '@gmail.com' at the end.
 Print 'Valid Gmail' if it matches, otherwise print 'Invalid Gmail'.'''

import re

email = input("Enter Gmail address: ")

pattern = r'^[a-z].*@gmail\.com$'

if re.match(pattern, email):
    print("Valid Gmail")
else:
    print("Invalid Gmail")