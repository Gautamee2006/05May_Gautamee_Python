'''Build a class Payment with a pay() method that takes amount as a parameter and
 prints 'Paying amount'. Then, create a subclass UPI that overrides pay() to
 print 'Paying amount via UPI'. Demonstrate both methods by making objects and calling pay().'''

class Payment:
    def pay(self, amount):
        print("Paying", amount)


class UPI(Payment):
    def pay(self, amount):
        print("Paying", amount, "via UPI")


# Objects
p = Payment()
u = UPI()

# Method calls
p.pay(1000)
u.pay(1000)