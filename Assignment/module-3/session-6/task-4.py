'''Implement multiple inheritance by creating a class BrandPartner that inherits from both
 Influencer and a new class Brand (with attribute brand_name); create a BrandPartner object 
 and print the username, followers, and brand_name.'''

class Influencer:
    username="gautamee"
    followers=1000

class Brand:
    brand_name="nike"

class BrandPartner(Influencer,Brand):
    def show(self):
        print("username:",self.username)
        print("email:",self.followers)
        print("brand name:",self.brand_name)

bp=BrandPartner()
bp.show()