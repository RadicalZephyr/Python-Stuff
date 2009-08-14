import os, sys, shutil, time, id3
from os.path import join

class FileInfo(dict):
    "store file metadata"
    def __init__(self, filename=None):
        self["name"] = filename
    
class MP3FileInfo(id3.ID3):
    def __init__(self, *args, **kwargs):
        id3.ID3.__init__()
        

class M4AFileInfo(id3.ID3):
    def __init__(self, *args, **kwargs):
        id3.ID3.__init__()

class MP4FileInfo(id3.ID3):
    def __init__(self, *args, **kwargs):
        id3.ID3.__init__()
        

def listDirectory(directory, fileExtList):
    "get list of file info objects for files of particular extensions"
    fileList = [os.path.normcase(f) for f in os.listdir(directory)]
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]
    def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):
        "get file info class from filename extension"
        subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]
        return hasattr(module, subclass) and getattr(module, subclass) \
               or FileInfo
    return [getFileInfoClass(f)(f) for f in fileList]

# From here down is my own work.
def getExtList(ftype):
    if str(ftype).startswith('.'): # If it's a string of a single filetype return a list
        return [ftype]
    elif str(ftype).startswith('['): # If it's a list, return the list
        return ftype
    elif ftype == 'audio':
        return ['.mp2','.mp3', '.m4a', '.ogg','.flac','.aac','.wma','.wav']
    elif ftype == 'video':
        return ['.avi','.divx','.mp4','.ogm','.qt','.wmv','.mov']
    elif ftype == 'text':
        return ['.txt','.doc','.docx','.odt','.rtf']
    elif ftype == 'prog':
        return ['.py','.c','.pl']
    
class fileMover:
    "move all files of ftype from one root directory"
    def __init__(self, ftype):
        self.type = ftype                   # Setup the needed variables
        self.extList = getExtList(ftype)
        self.fileList = []
        
    def fileFind(self, dir):
        """
        Search through a directory tree looking for the
        filetype this class was instantiated to look for
        """
        for root, dirs, files in os.walk(dir):
                map(self.fileList.append, listDirectory(root, self.extList))

    def makeNewDir(self, dir):
        "Make sure that the paths needed for self.fileMove exist"
        for fObject in self.fileList:
            try:
                os.makedirs(join(dir,self.type))
            except WindowsError:
                pass

    def fileMove(self, dir):
        "Move files in self.fileList to dir"
        for fObject in self.fileList:
            shutil.move(fObject['name'], dir)
            
class AUDIOMover(fileMover):
    "move and organize audio files" 
    def __init__(self, ftype='audio'):
        fileMover.__init__(self, ftype)

#    def makeNewDir(self, dir):
#        "Make sure that the paths needed for self.fileMove exist"
#        for fObject in self.fileList:
#            try:
#                os.makedirs(join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
#            except WindowsError:
#                pass

    def fileMove(self, dir, delsrc=False):
        "Move files in self.fileList to dir"
        move = delsrc and shutil.move or shutil.copy2
        for fObject in self.fileList:
            try: move(fObject['name'],
                      join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
            except IOError:
                try: os.makedirs(join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
                except WindowsError: pass
                move(fObject['name'],
                      join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
                # The above block should make the commented code obsolete...
##        if delsrc == True:
##            for fObject in self.fileList:
##                try:
##                    shutil.move(fObject['name'],
##                                join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
##                except IOError:
##                    try:
##                        os.makedirs(join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
##                    except WindowsError:
##                        pass
##                    shutil.move(fObject['name'],
##                                join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
##        else:
##            for fObject in self.fileList:
##                if 'title' in fObject.keys():
##                    try:
##                        shutil.copy2(fObject['name'], join(dir,str(fObject.get('artist')),
##                                                           str(fObject.get('album')),
##                                                           "".join((str(fObject.get('title')),
##                                                                         str(os.path.splitext(fObject['name'])[1])))))
##                    except IOError:
##                        print "Failed to copy, title"
##                else:
##                    try:
##                        shutil.copy2(fObject['name'], join(dir,str(fObject.get('artist')),
##                                                           str(fObject.get('album')),str(fObject.get('artist'))))
##                    except IOError:
##                        print "Failed to copy, no title"

    def fileMoveAlbum(self, dir):
        "Move files in self.fileList to dir"
        for fObject in self.albumCrossList:
            try:
                shutil.move(fObject['name'],join(dir,str(fObject.get('album'))))
            except IOError:
                try:
                    os.makedirs(join(dir,str(fObject.get('album'))))
                except WindowsError:
                    pass
                shutil.move(fObject['name'],join(dir,str(fObject.get('album'))))

    def albumCheck(self, dir):
        "Check through dir for albums with only one song"
        self.albumCrossList = []
        for root, dirs, files in os.walk(dir):
            fileObs = listDirectory(root, self.extList)
            if len(fileObs) == 1:
                self.albumCrossList.append(fileObs[0])
        def albumCrossCheck():
            "Check if songs that have their own folder really should"
            self.albumList = []
            for fObject in self.albumCrossList:
                self.albumList.append(fObject.get('album')) # Create a list of album names to cross check
            self.albumCrossList.sort()
            for item in self.albumList:
                if not self.albumList.count(item) > 1:  # Unless there's more than one reference to that album
                    self.albumList.remove(item)         # get rid of it.
            for fObject in self.albumCrossList:
                if fObject.get('album') not in self.albumList:  # Update the file object list to reflect album cross referencing
                    self.albumCrossList.remove(fObject)
        albumCrossCheck()

    def cleanUp(self, dir):
        for root, dirs, files in os.walk(dir, topdown=False):
            if not files+dirs:
                os.removedirs(root)

def yesOrNo(prompt):
    """Takes a prompt for a y/n answer"""
    answer = restrictedInput(prompt, 'Y', 'y', 'N', 'n')
    if answer.Upper() == 'Y':
        return True
    elif answer.Upper() == 'N':
        return False

def restrictedInput(prompt, *outputs):
    """Take a prompt and list of acceptable inputs, only returns user's input when they enter something valid"""
    while True:
        answer = raw_input(prompt)
        if answer in outputs:
            return answer
        else:
            print "Invalid input, please try again:"
        
                

if __name__ == "__main__":
    def menu():
        print "1) Move Files"
        print "2) Perform Album Check"
        print "3) Cleanup a Directory"
        print "4) Exit"
        
    menuChoice = 0
    
    while True:
        amove = AUDIOMover()
        menu()
        menuChoice = raw_input("Input Option: ")
        if menuChoice == '1':
            source = os.path.normpath(raw_input("Input source folder path: "))
            dest = os.path.normpath(raw_input("Input destination folder path: "))
            delchoice = yesOrNo("Delete old files?")
            amove.fileFind(source)
    #        amove.makeNewDir(dest)
            amove.fileMove(dest, delchoice)
            print "%d files were moved from %s to %s" % (len(amove.fileList), source, dest)
            print '\n' * 3
        elif menuChoice == '2':
            root = os.path.normpath(raw_input("Input folder to check albums of: "))
            amove.albumCheck(root)
            amove.fileMoveAlbum(root)
            print root + "was resorted by album."
            print '\n' * 3
        elif menuChoice == '3':
            clean = os.path.normpath(raw_input("Input folder to clean up: "))
            amove.cleanUp(clean)
            print clean + "was cleaned up."
            print '\n' * 3
        elif menuChoice == '4':
            print "Thank you."
            time.sleep(2.2)
            break