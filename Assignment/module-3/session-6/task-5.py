'''Refactor your VerifiedInfluencer class to include a method display_profile() that prints 
details in the format used on Instagram profiles (username, followers in K/M, badge status).
<br><br><em><strong>Hint:</strong> Use a helper function to format large follower counts, 
e.g., 1500 as '1.5K'.</em>'''

class Influencer:
    def format_followers(self):
        if self.followers>=1000000:
            return str(self.followers/1000000)+"M"
        elif self.followers>=1000:
            return str(self.followers/1000)+"K"
        else:
            return str(self.followers)
        
class VerifiedInfluencer(Influencer):
    def display_profile(self):
        print()
        print("-----instagram Profile:-----")
        print("username:",self.username)
        print("followers:",self.format_followers())

        if self.verified.lower()=="yes":
            print("Badge: verified ")
        else:
            print("Budge: not verified")

v=VerifiedInfluencer()

v.username=input("enter your usename:")
v.followers=int(input("enter your followers:"))
v.verified=input("verified(yes/no):")

v.display_profile()