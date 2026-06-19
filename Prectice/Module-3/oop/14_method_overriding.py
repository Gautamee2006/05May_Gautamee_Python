class master:
    def signin(self,unm,pas):
        if unm=="admin" and pas=="admin":
            print("login succesfulluy!")
        else:
            print("error!")

class home(master):
    def signin(self, unm, pas):
        return super().signin(unm, pas)
    
class shop(master):
    def signin(self, unm, pas):
        return super().signin(unm, pas)
    
h=home()
h.signin("admin","admin")