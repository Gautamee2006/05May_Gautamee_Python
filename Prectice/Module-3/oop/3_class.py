class studinfo:
    stid=0
    stnm=''

    def getdata(self):
        self.stid=input("enter your id:")        
        self.stnm=input("enter your name:")

    def showdata(self):
        print("id:",self.stid)
        print("name:",self.stnm)     

s=studinfo()
s.getdata()
s.showdata()