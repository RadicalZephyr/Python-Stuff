def element_clickMotion(self, eEvent):
        #.winfo_rootx/y = x,y position from top left of MONITER
        #.winfo_x/y = x,y position from top left of CONTAINER
        global wLastClicked, document_elements,mouseX, mouseY, wWidgetInMotion

        #This simply checks the widget the user has clicked is within the canvas and thus OK to drag.
        if bElementMoving == True: #Flag from <Button-1> binding
            if wWidgetInMotion == None:
                for element in document_elements: 
                    if wLastClicked == element[0]: #If the clicked widget is moveable i.e its on the canvas
                        wWidgetInMotion = wLastClicked
                        break

            if wWidgetInMotion <> None: #We did find a widget
                iCurrentx = wWidgetInMotion.winfo_x()
                iOffsetx = eEvent.x - mouseX
                iNewx = iCurrentx + iOffsetx

                iCurrenty = wWidgetInMotion.winfo_y()
                iOffsety = eEvent.y - mouseY
                iNewy = iCurrenty + iOffsety
                
                wWidgetInMotion.place(x=iNewx, y=iNewy)
                #^What this does is: position = position + pixel offset since last 'motion' event

                mouseX, mouseY = eEvent.x, eEvent.y #Bring to 'previous' position up to the 'current' position
            else: #No widget to move
                pass