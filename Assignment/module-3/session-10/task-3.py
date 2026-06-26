'''Arrange four buttons in a 2x2 grid layout using Tkinter's grid() method, similar to how
 calculator buttons are placed. Label the buttons as 'Like', 'Share', 'Download', and 'Add to Queue'.'''

import tkinter as tk

root = tk.Tk()
root.title("Music Controls")
root.geometry("300x200")

# Buttons in 2x2 Grid
b1 = tk.Button(root, text="Like", width=15)
b1.grid(row=0, column=0, padx=10, pady=10)

b2 = tk.Button(root, text="Share", width=15)
b2.grid(row=0, column=1, padx=10, pady=10)

b3 = tk.Button(root, text="Download", width=15)
b3.grid(row=1, column=0, padx=10, pady=10)

b4 = tk.Button(root, text="Add to Queue", width=15)
b4.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()