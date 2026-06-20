class student:
    stage=0
    stnm=''
    stmarks=0
    def getdata(self):
        self.stnm=input("enter your name:")
        self.stage=int(input("enter your age:"))
        self.stmarks=int(input("enter total of marks:"))

    def display(self):
        print("student name:",self.stnm)
        print("student age:",self.stage)
        print("student marks:",self.stmarks)

s=student()
s.getdata()
s.display()

file=open("student.txt",'w')
file.write(f"student name:{s.stnm}\nstudent age:{s.stage}\nstudent marks:{s.stmarks}")
file.read(student.txt)