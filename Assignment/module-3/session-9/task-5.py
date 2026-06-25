'''Use ChatGPT to generate a regular expression that matches Indian Railways PNR numbers 
(10-digit numbers), then implement a Python function is_valid_pnr(pnr) using re.match()
 to validate user input. Paste the regex and your function in your submission.'''

import re

def is_valid_pnr(pnr):
    if re.match(r'^\d{10}$', pnr):
        print("Valid PNR")
    else:
        print("Invalid PNR")


pnr = input("Enter PNR Number: ")
is_valid_pnr(pnr)
'''if is_valid_pnr(pnr):
    print("Valid PNR")
else:
    print("Invalid PNR")'''