'''Use re.search() to find and print the first 10-digit mobile number in a string that 
contains a mix of text and phone numbers, similar to how Zomato or Swiggy might display
contact info in reviews.'''

import re

text = input("Enter text: ")

result = re.search(r'\b\d{10}\b', text)

if result:
    print("Mobile Number Found:", result.group())
else:
    print("No Mobile Number Found")