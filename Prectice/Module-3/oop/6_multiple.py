class gautamee:
    gid:int
    gcourse:str

    def g_getdata(self):
        self.gid=input("enter gatu's id:")
        self.gcourse=input("enter gatu's course:")

class riya:
    raiseid:int
    rcourse:str

    def r_getdata(self):
        self.rid=input("enter riya's id:")
        self.rcourse=input("enter riya's course:")

class hinali:
    hid:int
    hcourse:str

    def h_getdata(self):
        self.hid=input("enter hinali's id:")
        self.hcourse=input("enter hinali's course:")

class tops(gautamee,riya,hinali):
    def display(self):
        print("----students data----")
        print("__!Gautamee's info!__")
        print("Gautamee's Id:",self.gid)
        print("Gautamee's course:",self.gcourse)
        print("__!Riya's info!__")
        print("Riya's Id:",self.gid)
        print("Riya's course:",self.gcourse)
        print("__!Hinali's info!__")
        print("Hinali's Id:",self.gid)
        print("Hinali's course:",self.gcourse)

tp=tops()
tp.g_getdata()
tp.r_getdata()
tp.h_getdata()
tp.display()