import tkinter
import sqlite3
from tkinter import messagebox

try:
    db=sqlite3.connect("demo.db")
    print("Database connected/created!")
except Exception as e:
    print(e)

#table create

tbl_create="create table stud(id integer primary key autoincrement,name varchar(20),email varchar(50),mobile int(10))"

try:
    db.execute(tbl_create)
    print("create table!")
except Exception as e:
    print(e)


tk=tkinter.Tk()
tk.title("NewApp")
tk.geometry("400x400")
tk.config(background="#9370DB")

l1=tkinter.Label(text="Name:",bg="#9370DB",fg="white",font='Courier 15 bold')
l1.grid(row=0,column=0,sticky='w')

l2=tkinter.Label(text="Email:",bg="#9370DB",fg="white",font='Courier 15 bold')
l2.grid(row=1,column=0,sticky='w')

l3=tkinter.Label(text="Mobile no:",bg="#9370DB",fg="white",font='Courier 15 bold')
l3.grid(row=2,column=0,sticky='w')

t1=tkinter.Entry()
t1.grid(row=0,column=1,sticky='w')
t2=tkinter.Entry()
t2.grid(row=1,column=1,sticky='w')
t3=tkinter.Entry()
t3.grid(row=2,column=1,sticky='w')

def btnClick():
    name=t1.get()
    email=t2.get()
    mobile=t3.get()

    if name=="" or email=="" or mobile=="":
        return messagebox.showerror("ERROR!","all fileds are required")
    
     # Email Validation
    if "@" not in email or "." not in email:
        return messagebox.showerror("Invalid Email","Enter a valid email address")

    # Mobile Validation
    if not mobile.isdigit():
        return messagebox.showerror("Invalid Mobile","Mobile number must contain only digits")

    if len(mobile) != 10:
        return messagebox.showerror("Invalid Mobile","Mobile number must be exactly 10 digits")

    try:
        qur="insert into stud(name,email,mobile)values(?,?,?)"
        db.execute(qur,(name,email,mobile))
        db.commit()
        print("record insert!")
        messagebox.showinfo("Success", "Data Inserted Successfully!")

         # Clear Entry Boxes
        t1.delete(0,tkinter.END)
        t2.delete(0,tkinter.END)
        t3.delete(0,tkinter.END)

    except Exception as e:
        messagebox.showerror("Database Error",e)

def showdata():
    try:
        cur=db.cursor()
        cur.execute("SELECT * FROM stud ORDER BY id DESC LIMIT 1")
        data=cur.fetchone()
        #print("\n----- STUDENT DATA -----")
        #data=cur.fetchone()
        #for i in data:
        #    print(i)
        messagebox.showinfo(
                "Your Details",
                f"ID : {data[0]}\n"
                f"Name : {data[1]}\n"
                f"Email : {data[2]}\n"
                f"Mobile No : {data[3]}"
        )

    except Exception as e:
        print(e)

btn=tkinter.Button(text="Submit",bg="#6A0DAD",fg="white",font='Courier 15 bold',command=btnClick)
btn.place(x=30,y=150)


btn1=tkinter.Button(text="Show data",bg="#6A0DAD",fg="white",font='Courier 15 bold',command=showdata)
btn1.place(x=150,y=150)

tk.mainloop()