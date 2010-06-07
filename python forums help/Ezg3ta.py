def Var(x):
    a = x.get()
    return a

from Tkinter import *

window = Tk()

v = IntVar()
g = v.trace("w", Var(v))

Radiobutton(window, text="Scale", variable=v, value=1).pack(side="left", padx=10)
Radiobutton(window, text="Entry", variable=v, value=2).pack(side="right", padx=10)

if g==1:
    size = Scale(window, from_=0, to=360, orient=HORIZONTAL)
    size.pack()

elif g==2:
    size = Entry(window)
    size.pack()    

window.mainloop()