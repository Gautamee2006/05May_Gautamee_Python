class account:

    def acc_data(self):
        self.ano=int(input("enter account no.:"))
        self.ahname=input("enter account holder name:")
        self.atype=input("enter account type:")

class deposite(account):

    def acc_amount(self):
        while True:
            self.amount = int(input("Enter deposit amount: "))

            if self.amount >= 2000:
                print("Deposit is done")
                return self.amount
            else:
                print("Minimum 2000 required")
    
class withdrwal(deposite):

    def acc_withdrwal(self):
        while True:
            m = float(input("enter withdrawal amount: "))

            if m <= self.amount:
                self.amount -= m
                print("Withdrawal successfuly")
                return self.amount
            else:
                print("insufficient balance")

class statement(withdrwal):

    def showdata(self):
        print("----account statement----")
        print("account no:",self.ano)
        print("account holder name:",self.ahname)
        print("account type:",self.atype)
        print("blance",self.amount)

s=statement()
s.acc_data()
s.acc_amount()
s.acc_withdrwal()
s.showdata()