'''Build a simple login form using Tkinter with two labels and two entry fields for 'Username' 
and 'Password', and a 'Login' button. When the button is clicked, display a message below saying
'Login Successful' if both fields are non-empty.<br><br><em><strong>Hint:</strong> Use the 
get() method of Entry widgets to read the input values.</em>'''

import tkinter as tk

root = tk.Tk()
root.title("Login Form")
root.geometry("400x300")
root.config(bg="#DCE3E8")   # Soft Gray Background

# Heading
title = tk.Label(
    root,
    text="Login Form",
    font=("Arial", 18, "bold"),
    bg="#DCE3E8",
    fg="#37474F"
)
title.pack(pady=15)

# Frame
frame = tk.Frame(root, bg="#F5F5F5", bd=2, relief="groove")
frame.pack(padx=20, pady=10)

# Username
tk.Label(frame, text="Username", bg="#F5F5F5",
         fg="#37474F", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10)

e1 = tk.Entry(frame, font=("Arial", 11), width=20)
e1.grid(row=0, column=1)

# Password
tk.Label(frame, text="Password", bg="#F5F5F5",
         fg="#37474F", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10)

e2 = tk.Entry(frame, show="*", font=("Arial", 11), width=20)
e2.grid(row=1, column=1)

# Message
msg = tk.Label(frame, text="", bg="#F5F5F5",
               font=("Arial", 11, "bold"))
msg.grid(row=3, column=0, columnspan=2, pady=10)

# Login Function
def login():
    user = e1.get()
    pwd = e2.get()

    if user != "" and pwd != "":
        msg.config(text="Login Successful", fg="green")

        # Clear Entry Fields
        e1.delete(0, tk.END)
        e2.delete(0, tk.END)

    else:
        msg.config(text="Please enter Username & Password", fg="red")

# Hover Effect
def enter(event):
    btn.config(bg="#78909C")

def leave(event):
    btn.config(bg="#90A4AE")

# Login Button
btn = tk.Button(
    frame,
    text="Login",
    font=("Arial", 11, "bold"),
    bg="#90A4AE",
    fg="white",
    width=15,
    command=login
)
btn.grid(row=2, column=0, columnspan=2, pady=10)

btn.bind("<Enter>", enter)
btn.bind("<Leave>", leave)

root.mainloop()