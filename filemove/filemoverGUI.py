# Filemover tkinterface

import filemover_mutagen as fmove
from Tix import *
import tkFileDialog, os

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.master = master

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
        self.sourceVar = StringVar()
        self.source = Entry(self)
        self.source.grid(row = 1, column = 3, sticky = W)
        self.source["textvariable"] = self.sourceVar

        self.selectSource = Button(self, text = "...",
                                   command = self.dirSelectSource)
        self.selectSource.grid(row = 1, column = 4, sticky = W)
        
        # Line Two
        Label(self, text = "Destination folder:")\
                    .grid(row = 2, column = 3, sticky = W)
        self.destVar = StringVar()
        self.dest = Entry(self)
        self.dest.grid(row = 3, column = 3, sticky = W)
        self.dest["textvariable"] = self.destVar

        self.selectDest = Button(self, text = "...",
                                 command = self.dirSelectDest)
        self.selectDest.grid(row = 3, column = 4, sticky = W)
        
        # Line Three
        self.findButton = Button(self, text = "Find files.",
                                 command = self.findFiles)
        self.findButton.grid(row = 3, column = 0)
        self.MoveButton = Button(self, text = "Move files.")
        self.MoveButton.grid(row = 3, column = 1)

        # Line Four
        self.foundFiles = Text(self, width = 50, height = 30,
                               wrap = WORD)
        self.foundFiles.grid(row = 4, column = 0, rowspan = 4,
                             columnspan = 4, sticky = W)

    def findFiles(self):
        if self.AudioCheck.get():
            self.audiomove = fmove.AUDIOMover()
            self.audiomove.fileFind(self.sourceVar.get())
            self.foundFiles.insert(END, '/n'.join([file["name"] for file in self.audiomove.fileList]))
            
        typelist = self.checkCheckBoxes()
        if typelist:
            self.filemove = fmove.fileMover(typelist)
            self.filemove.fileFind(self.sourceVar.get())
            self.foundFiles.insert(END, '/n'.join([file["name"] for file in self.filemove.fileList]))
        
        


    def checkCheckBoxes(self):
        fileMovers = []
        if self.VideoCheck.get():
            fileMovers.append(self.VideoCheck.get())
        if self.TextCheck.get():
            fileMovers.append(self.TextCheck.get())
        if self.ProgCheck.get():
            fileMovers.append(self.ProgCheck.get())
        return fileMovers

    def dirSelectSource(self):
        self.dirSelectWindow(self.sourceVar)

    def dirSelectDest(self):
        self.dirSelectWindow(self.destVar)

    def dirSelectWindow(self, boxvar):
        boxvar.set(os.path.normpath(tkFileDialog.askdirectory(parent = self.master,
                                             initialdir = '/')))
                                  


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