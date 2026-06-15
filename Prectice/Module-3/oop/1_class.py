class BCA:
    stid=20
    stname="gautamee"

    def getdata(self):
        print("this is a class")

    def sum(self,a,b):
        print("sum is:",a+b)

bca=BCA()
print("student id:",bca.stid)
print("student name:",bca.stname)
bca.getdata()
bca.sum(12,23)