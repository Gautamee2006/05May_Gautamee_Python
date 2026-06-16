class login:
    def __init__(self,unm,pas):
        if unm=="admin" and pas=="admin":
            print("login successfully")
        else:
            print("error!")

unm=input("enter name:")
pas=input("enter password:")
l=login(unm,pas)