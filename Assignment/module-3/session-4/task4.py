'''Given the following traceback from a Python program, use ChatGPT to explain in your own words
 what the error means and how you would fix it:<br><br>Traceback (most recent call last):<br> File 
 "main.py", line 8, in <module><br> book_ticket('Avengers', -2)<br> File "main.py", line 4, 
 in book_ticket<br> raise InvalidSeatNumberError('Seat number must be positive')
 <br>NameError: name 'InvalidSeatNumberError' is not defined'''



'''The error occurs because the program tries to raise InvalidSeatNumberError, but this custom 
exception class has not been defined. Python cannot recognize the name, so it raises a NameError. 
To fix the error, define the InvalidSeatNumberError class before using it in the raise statement.'''

'''class InvalidSeatNumberError(Exception):
    pass'''

def book_ticket(movie,seat_no):
    if seat_no<=0:
        raise InvalidSeatNumberError("seat number must be positive")
    else:
        print("Ticket book sucessfuly for",movie)

movie=input("emter movie name:")
seat_no=int(input("enter seat number:"))

try:
    book_ticket(movie,seat_no)
except InvalidSeatNumberError as e:
    print(e)