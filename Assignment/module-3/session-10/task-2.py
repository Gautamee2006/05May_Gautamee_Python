'''Add three buttons to your Tkinter window labeled 'Play', 'Pause', and 'Next'. When each button 
is clicked, update a label below the buttons to show which action was selected 
(e.g., 'Playing', 'Paused', 'Next Song').'''

import tkinter as tk

root = tk.Tk()
root.title("My Playlist")
root.geometry("400x200")

# Heading
l1 = tk.Label(root, text="Welcome to Your Music Playlist", font=("Arial", 14))
l1.grid(row=0, column=0, columnspan=3, pady=10)

# Functions
def play():
    status.config(text="Playing")

def pause():
    status.config(text="Paused")

def next():
    status.config(text="Next Song")

# Buttons
b1 = tk.Button(root, text="Play", width=10, command=play)
b1.grid(row=1, column=0, padx=5)

b2 = tk.Button(root, text="Pause", width=10, command=pause)
b2.grid(row=1, column=1, padx=5)

b3 = tk.Button(root, text="Next", width=10, command=next)
b3.grid(row=1, column=2, padx=5)

# Status Label (Buttons ke neeche)
status = tk.Label(root, text="Status", font=("Arial", 12))
status.grid(row=2, column=0, columnspan=3, pady=15)

root.mainloop()