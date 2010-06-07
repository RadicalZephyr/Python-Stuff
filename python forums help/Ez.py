from Tkinter import *


def updateWidgets(event=None):
    g = v.get()
    scale.pack_forget()
    size.pack_forget()
    if g == 1:
        scale.pack()
    elif g == 2:
        size.pack()

window = Tk()
v = IntVar()

size = Entry(window)
scale = Scale(window, from_=0, to=360, orient=HORIZONTAL)

a = Radiobutton(window, text="Scale", variable=v, value=1, command=updateWidgets)
a.pack(side="left", padx=10)
b = Radiobutton(window, text="Entry", variable=v, value=2, command=updateWidgets)
b.pack(side="right", padx=10)

window.mainloop()