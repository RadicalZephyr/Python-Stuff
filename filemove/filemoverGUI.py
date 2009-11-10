# Filemover tkinterface

import filemover_mutagen as fmove
import filemoverhelper as fhelp
from Tkinter import *



class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        #Line Zero
        Label(self, text = "File type(s):")\
                    .grid(row = 0, column = 0, sticky = W)
        
        # Checkbutton Variables
        self.AudioCheck = StringVar(value='')
        self.VideoCheck = StringVar(value='')
        self.ProgCheck = StringVar(value='')
        self.TextCheck = StringVar(value='')

        # Checkbuttons
        Checkbutton(self, text = 'Audio',
                    variable = self.AudioCheck,
                    offvalue = '',
                    onvalue = 'audio',
                    ).grid(row = 1, column = 0, sticky = W)
        Checkbutton(self, text = 'Video',
                    variable = self.VideoCheck,
                    offvalue = '',
                    onvalue = 'video',
                    ).grid(row = 1, column = 1, sticky = W)
        Checkbutton(self, text = 'Text',
                    variable = self.TextCheck,
                    offvalue = '',
                    onvalue = 'text',
                    ).grid(row = 2, column = 0, sticky = W)
        Checkbutton(self, text = 'Programming',
                    variable = self.ProgCheck,
                    offvalue = '',
                    onvalue = 'prog',
                    ).grid(row = 2, column = 1, sticky = W)
                
        # Line One
        Label(self, text = "Source folder:")\
                    .grid(row = 0, column = 3, sticky = W)
        self.source = Entry(self)
        self.source.grid(row = 1, column = 3, sticky = W)
        
        # Line Two
        Label(self, text = "Destination folder:")\
                    .grid(row = 2, column = 3, sticky = W)
        self.dest = Entry(self)
        self.dest.grid(row = 3, column = 3, sticky = W)
        
        # Line Three
        self.findButton = Button(self, text = "Find files.",
                                 command = self.updateBox)
        self.findButton.grid(row = 3, column = 0)
        self.MoveButton = Button(self, text = "Move files.")
        self.MoveButton.grid(row = 3, column = 1)

        # Line Four
        self.foundFiles = Text(self, width = 50, height = 30,
                               wrap = WORD)
        self.foundFiles.grid(row = 4, column = 0, rowspan = 4,
                             columnspan = 4, sticky = W)
    def initMover(self):
        pass#self.fileMover = filemove.

# Development Tool, remove before use/deployment
    def updateBox(self):
        vartotal = [self.AudioCheck.get(), self.VideoCheck.get(), \
                   self.TextCheck.get(), self.ProgCheck.get()]
        self.foundFiles.delete(0.0, END)
        self.foundFiles.insert(0.0, '\n'.join(vartotal))


tk = Tk()
tk.title("File Mover")
tk.geometry("400x500")

Window = Application(tk)

tk.mainloop()