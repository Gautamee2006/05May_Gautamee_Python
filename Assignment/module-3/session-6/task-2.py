'''Build a single inheritance example where a class Influencer inherits from User and adds a
 followers attribute; create an Influencer object and print all its details.'''

class User:
    username:str
    email:str

class Influencer(User):
    followers:int

i=Influencer()

i.username=input("enter usename:")
i.email=input("enter email:")
i.followers=int(input("enter your followers:"))

print()
print("------all details:------")
print("username:",i.username)
print("email:",i.email)
print("followers:",i.followers)