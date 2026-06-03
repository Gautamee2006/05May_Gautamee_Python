def ac_detail(no, name, type, amount=0):
    return no, name, type, amount


def deposite(amount):

    if amount >= 2000:
        print("deposite is done")
    else:
        print("minimum 2000 required")

    return amount


def withdwal(amount):

    m = float(input("enter withdrawal amount: "))

    if m <= amount:
        total = amount - m
        return total
    else:
        print("insufficient balance")
        return amount


def statement():

    no = int(input("enter account no: "))
    name = input("enter holder name: ")
    type = input("enter account type: ")
    amount = float(input("enter deposite amount: "))

    ac_detail(no, name, type, amount)

    deposite(amount)

    balance = withdwal(amount)

    print("\nAccount Detail")
    print("account number :", no)
    print("holder name :", name)
    print("account type :", type)
    print("total balance :", balance)


statement()