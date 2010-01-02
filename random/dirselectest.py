##from Tix import *
##
##tk = Tk()
##
####def show():
####    print textVar1
####    
####dialog = DirSelectDialog(tk, command = show)
####dialog.popup()
####
####print dialog.subwidgets_all()
####textVar1 = StringVar()
####dialog["textvariable"] = textVar1
##import tkFileDialog
##
##dirname = tkFileDialog.askdirectory()
##
##tk.mainloop()


import Tkinter, tkFileDialog

root = Tkinter.Tk()
dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
if len(dirname ) > 0:
    print "You chose %s" % dirname 