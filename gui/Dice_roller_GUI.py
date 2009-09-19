################################################################
#Dice_roller_GUI
#
#Purpose:  Provide a graphical interface to the dice_roller module; 
#   allow various die rolls using the mouse.  This program uses the Tkinter
#   GUI module that is included with Python.  Requires Python 2.3+ to be
#   installed.
#Author: Cody Jackson
#Date: 6/1/06
#
#Copyright 2006 Cody Jackson
#This program is free software; you can redistribute it and/or modify it 
#under the terms of the GNU General Public License as published by the Free 
#Software Foundation; either version 2 of the License, or (at your option) 
#any later version.
#
#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranty of 
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#General Public License for more details.
#
#You should have received a copy of the GNU General Public License 
#along with this program; if not, write to the Free Software Foundation, 
#Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
#----------------------------------------------------------------
#Version 1.0
#   Initial build
#################################################################
from Tkinter import *
from dice_roller import multiDie

class DiceRoll(Frame):
    """Dice rolling simulation program."""
    
    def __init__(self):
#---Frame is the "container" for rest of code
        Frame.__init__(self)
        self.pack(expand = YES, fill = BOTH)    #Frame fills all available space
        self.master.title("Dice roll simulation")
        
#---Create buttons for each type of die roll
        self.button1d6 = Button(self, text = "1d6", command = self.pressed1d6)
        self.button1d6.grid(row = 0, column = 0) #stack d6 buttons vertically
        
        self.button2d6 = Button(self, text = "2d6", command = self.pressed2d6)
        self.button2d6.grid(row = 1, column = 0)
        
        self.button3d6 = Button(self, text = "3d6", command = self.pressed3d6)
        self.button3d6.grid(row = 2, column = 0)
        
        self.button1d10 = Button(self, text = "1d10", command = self.pressed1d10)
        self.button1d10.grid(row = 0, column = 1) #stack d10 buttons next to d6 buttons
        
        self.button2d10 = Button(self, text = "2d10", command = self.pressed2d10)
        self.button2d10.grid(row = 1, column = 1)
        
        self.button1d100 = Button(self, text = "1d100 (%)", command = self.pressed1d100)
        self.button1d100.grid(row = 2, column = 1)
        
#---Create message area
        self.result = StringVar()
        self.resultLine = Label(self, textvariable = self.result)
        self.result.set("Die roll")
        self.resultLine.grid(row = 1, column = 2)
        
#---Define button methods    
    def pressed1d6(self):
        """Roll one 6-sided die."""
        
        self.result.set(multiDie(1,1))
        
    def pressed2d6(self):
        """Roll two 6-sided dice."""

        self.result.set(multiDie(2,1))

    def pressed3d6(self):
        """Roll three 6-sided dice."""

        self.result.set(multiDie(3,1))

    def pressed1d10(self):
        """Roll one 10-sided die."""

        self.result.set(multiDie(1,2))

    def pressed2d10(self):
        """Roll two 10-sided dice."""

        self.result.set(multiDie(2,2))

    def pressed1d100(self):
        """Roll one 100-sided die or roll a percentage."""

        self.result.set(multiDie(1,3))

def main():
    DiceRoll().mainloop()

if __name__ == "__main__":
    main()