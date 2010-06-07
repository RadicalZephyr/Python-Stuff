# htmlGenEd extensions
from simpleText import SimpleEditor
from Tkinter import *
import sys

class htmlEditor(SimpleEditor):
    def __init__(self, parent=None, file=None):
        SimpleEditor.__init__(self, parent, file)
        Button(self.frm, text="I", command=self.italics).pack(side=LEFT)
        Button(self.frm, text="U", command=self.underline).pack(side=LEFT)
        Button(self.frm, text="B", command=self.bold).pack(side=LEFT)
    def italics(self):
        pass
    def underline(self):
        pass
    def bold(self):
        pass

if __name__ == "__main__":
    try:
        htmlEditor(file=sys.argv[1]).mainloop()
    except IndexError:
        htmlEditor().mainloop()
