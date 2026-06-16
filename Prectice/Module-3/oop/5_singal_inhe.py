class father:
    car:int
    bln:int

    def getdata(self):
        self.car=int("how many cars? ")
        self.bln=int("what is your account balance? ")

class son(father):
    def showdata(self):
        print("cars:",self.car)
        print("balance:",self.bln)

s=son()
s.getdata()
s.showdata()