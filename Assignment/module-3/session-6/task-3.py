'''Demonstrate multilevel inheritance by creating a class VerifiedInfluencer that inherits 
from Influencer and adds a badge attribute; create a VerifiedInfluencer object and display 
all its properties.'''

class user:
    username="Gautamee"
    email="gautamee@gamil.com"

class Influencer(user):
    followers=1000

class verifiedInfluencer(Influencer):
    badge="blue tick"

v=verifiedInfluencer()
print("username",v.username)
print("email:",v.email)
print("followers:",v.followers)
print("bage:",v.badge)