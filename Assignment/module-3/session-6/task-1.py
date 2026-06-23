'''Create a Python class called User with attributes username and email, 
then create an object and print its details.'''

class User:
    def __init__(self,username,email):
        self.username=username
        self.email=email

u=User("Gautamee","gautamee@gmail.com")

print("username:",u.username)
print("email:",u.email)