# Filemover tkinterface

import filemover_mutagen, filemoverhelper
from Tkinter import *

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        Label(self, text = "Source folder:")\
                    .grid(row = 0, column = 0, sticky = W)
        self.source = Entry(self)
        self.source.grid(row = 0, column = 1, sticky = W)
        Label(self, text = "Destination folder:")\
                    .grid(row = 1, column = 0, sticky = W)
        self.dest = Entry(self)
        self.dest.grid(row = 1, column = 1, sticky = W)
        self.moveButton = Button(self, text = "Move audio files.")
        self.moveButton.grid(row = 2, column = 1)



_selectedDirectory = None
_dirList = None
_fileList = None
_gotoEntry = None

tk = Tk()

Window = Application(tk)