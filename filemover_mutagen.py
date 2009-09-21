# What's next: implement a file cleanup that finds files with identical tags, and deletes or at least finds one copy.
# have a folder clean that finds similarly tagged files and deletes one  on
# the basis of bitrate
# Also have one that makes a list of filename's/paths of low bitrate songs.


import os, sys, shutil, time, id3
from os.path import join
from Gtoolbox import *

# This is from Mark Pilgrim's Diveintopython
class FileInfo(dict):
    """store file metadata"""
    def __init__(self, filename=None):
        self["name"] = filename

def listDirectory(directory, fileExtList):
    """Get list of file info objects for files of particular extensions"""
    fileList = [os.path.normcase(f) for f in os.listdir(directory)]
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]
    def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):
        """Get file info class from filename extension"""
        subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]
        return hasattr(module, subclass) and getattr(module, subclass) \
               or FileInfo
    return [getFileInfoClass(f)(f) for f in fileList]

# From here down is my own work.
class ID3FileInfo(id3.ID3):
    def __init__(self, *args, **kwargs):
        id3.ID3.__init__(args, kwargs)
        self["name"] = args[0]
        self["album"] = sanitizePath(self.get("TALB"))
        self["title"] = sanitizePath(self.get("TIT2"))
        self["artist"] = sanitizePath(self.get("TPE1") or self.get("TPE2"))
        self["tracknum"] = sanitizePath(self.get("TRCK"))

class MP3FileInfo(ID3FileInfo):
    """Wrapper class for ID3FileInfo to interact with listDirectory"""
    pass

class M4AFileInfo(ID3FileInfo):
    """Wrapper class for ID3FileInfo to interact with listDirectory"""
    pass

class MP4FileInfo(ID3FileInfo):
    """Wrapper class for ID3FileInfo to interact with listDirectory"""
    pass

def getExtList(ftype):
    ftypeString = str(ftype)
    if ftypeString.startswith('.'): # If it's a string of a single filetype return a list
        return [ftype]
    elif ftypeString.startswith('['): # If it's a list, return the list
        return ftype
    elif ftype == 'audio':
        return ['.mp2','.mp3', '.m4a', '.ogg','.flac','.aac','.wma','.wav']
    elif ftype == 'video':
        return ['.avi','.divx','.mp4','.ogm','.qt','.wmv','.mov']
    elif ftype == 'text':
        return ['.txt','.doc','.docx','.odt','.rtf']
    elif ftype == 'prog':
        return ['.py','.c','.pl']
    else:
        print >> sys.stderr, "ftype not defined."
    
class fileMover:
    """Provides basic file moving capabilities for files of ftype

    More advanced capabilities and options can be obtained using the
    child classes, AUDIOMover etc."""

    def __init__(self, ftype):
        self.type = ftype                   # Setup the needed variables
        self.extList = getExtList(ftype)
        self.fileList = []
        self.folderList = []
        self.delsrc = None

    def fileFind(self, dir):
        """Find files of self.ftype

        Search through a directory tree looking for the
        filetype this class was instantiated to look for.
        """
        for root, dirs, files in os.walk(dir):
                map(self.fileList.append, listDirectory(root, self.extList))
                # This part should check if there are any of ftype in the folder, and if there
                # are put the folder in self.folderList. This method is klugey and should be
                # integrated with the above map in some fashion.
                
                
# This is obsolete.
##    def makeNewDir(self, dir):
##        """Make sure that the paths needed for self.fileMove exist"""
##        for fObject in self.fileList:
##            try:
##                os.makedirs(join(dir,self.type))
##            except WindowsError:
##                pass

    def fileMove(self, dir):
        """Move files in self.fileList to dir"""
        for fObject in self.fileList:
            try: os.makedirs(join(dir,self.type))
            except: pass
            shutil.move(fObject['name'], dir)
            
class AUDIOMover(fileMover):
    "move and organize audio files" 
    def __init__(self, ftype='audio'):
        fileMover.__init__(self, ftype)

##    def makeNewDir(self, dir):
##        "Make sure that the paths needed for self.fileMove exist"
##        for fObject in self.fileList:
##            try:
##                os.makedirs(join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
##            except WindowsError:
##                pass
# This doesn't work how I intended it to originally.
# After rewriting, I think this is both obsolete and unworkable...
##    def buildDirString(self, dir, organization):
##        for str in organization:
##            dir = join(dir, str)
##        return dir

    def fileMove(self, dir, fileList=None, delsrc=False, organization=["artist", "album"]):
        """Move files in self.fileList to dir"""
        self.delsrc = delsrc # Record for undo option.
        self.lastDest = dir
        
        move = delsrc and shutil.move or shutil.copy # Check delsrc flag
##        dir = buildDirString(dir, organization)        
        if fileList == None:    # See if there was another fileList given
            fileList = self.fileList    # if not, use the default

        for fObject in fileList:
            for item in organization:    # Build the directory string recursively
                dir = join(dir, fObject.get(item))
                
            fObject['undoInfo'] = (join(dir, os.path.split(fObject['name'])[1]), \
                                       fObject['name']) # Record for easing undo
# This seems inefficient.
##            try: move(fObject['name'], dir) # Do the actual moving
##            except IOError:     # This probably means the folders don't exist
##                try: os.makedirs(dir)   # So make them, and try again.
##                except WindowsError: pass
##                move(fObject['name'], dir)
# This should be better than the above commented out code
            try: os.makedirs(dir)   # Try to make the new directories
            except WindowsError: pass
            move(fObject['name'], dir) # Do the actual moving

# The above block should make the commented code obsolete...
##        if delsrc == True:
##            for fObject in.fileList:
##                try:
##                    shutil.move(fObject['name'],
##                                join(dir,str(fObject.get('artist')),
##                                     str(fObject.get('album'))))
##                except IOError:
##                    try:
##                        os.makedirs(join(dir,str(fObject.get('artist')),
##                                         str(fObject.get('album'))))
##                    except WindowsError:
##                        pass
##                    shutil.move(fObject['name'],
##                                join(dir,str(fObject.get('artist')),
##                                     str(fObject.get('album'))))
##        else:
##            for fObject in self.fileList:
##                if 'title' in fObject.keys():
##                    try:
##                        shutil.copy2(fObject['name'], 
##                                     join(dir,str(fObject.get('artist')),
##                                                   str(fObject.get('album')),
##                                                   "".join((str(fObject.get('title')),
##                                                   str(os.path.splitext(fObject['name'])[1])))))
##                    except IOError:
##                        print "Failed to copy, title"
##                else:
##                    try:
##                        shutil.copy2(fObject['name'], 
##                                     join(dir,str(fObject.get('artist')),
##                                                  str(fObject.get('album')),
##                                                  str(fObject.get('artist'))))
##                    except IOError:
##                        print "Failed to copy, no title"

# This function may be obsolete because of the added functionality of fileMove and the end of albumCheck.
##    def fileMoveAlbum(self, dir):
##        "Move files in self.fileList to dir"
##        self.albumCheck(dir)
##        for fObject in self.albumCrossList:
##            dir = buildDirString(dir, fObject.get("album"))
##
##            try:
##                shutil.move(fObject['name'], dir)
##            except IOError:
##                try:
##                    os.makedirs(dir)
##                except WindowsError:
##                    pass
##                shutil.move(fObject['name'], dir)

    def albumCheck(self, dir):
        """Check through dir for albums with only one song

        Only works on directories that have already been organized with
        fileMove"""
        self.albumCrossList = []
        for root, dirs, files in os.walk(dir):
            fileObs = listDirectory(root, self.extList)
            if len(fileObs) == 1: # If there's only one song in a folder
                self.albumCrossList.append(fileObs[0]) # Add it to the list to check.
        self.albumList = []
        for fObject in self.albumCrossList:
            self.albumList.append(fObject.get('album')) 
# Create a list of album names to cross check
        self.albumCrossList.sort()
        for item in self.albumList:
            if not self.albumList.count(item) > 1:  
# Unless there's more than one reference to that album
# get rid of it.
                self.albumList.remove(item)         
        for fObject in self.albumCrossList:
            if fObject.get('album') not in self.albumList:  
# Update the file object list to reflect album cross referencing
                self.albumCrossList.remove(fObject)
        self.fileMove(dir, organization=["album"], fileList=self.albumCrossList)

##    def findDoubles(self, bitrate=128, fileList=None):
##        if fileList == None:
##            fileList = self.fileList
##        doubleList = []
##        for root, dirs, files in os.walk(dir):

    def doubleCheck(self, dir):
        """Check a directory for duplicate files

        Optional flags for checking by length, filename, ID3 tags"""
        fileFind(dir)
        doubleCheckList = []
        for fObject in self.fileList:
            

    def undoMove(self):
        """Undo the last fileMove operation."""

        if not self.delsrc: # If the originals weren't deleted, don't try and move
            delSongs(self.lastDest)   # just clean up the dest folder.
        else:
            for fObject in self.fileList:   # Otherwise, just reverse the move.
                try: os.makedirs(dir)
                except WindowsError: pass
                shutil.move(fObject["undoInfo"])

        
        
    def printList(self, filelist=None):
        """Print the fileList in a human-readable form"""
        self.readableList = []
        tempList = []
        
        if fileList == None:
            fileList = self.fileList

        for fObject in fileList:
            self.readableList.append((str(fObject.get('title')), str(fObject.get('artist')), \
                                      str(fObject.get('album')), str(fObject.get('name'))))

        for item in self.readableList:
            tempList.append("%s by %s on %s; named %s" % item) 
            self.prettyString = '\n'.join(tempList)
            return self.prettyString

    def fileCleanUp(self, dir):
        """Delete all the music files in a folder."""
        self.fileFind(dir)
        for fObject in self.fileList: os.remove(fObject["name"])

    def folderCleanUp(self, dir):
        for root, dirs, files in os.walk(dir, topdown=False): # Go to the leaf.
            if not files+dirs:      # If there's nothing in that folder try to delete it.
                try:
                    os.removedirs(root) # This will go upwards deleting empty folders automatically
                except OSError:         # but it can never delete a non-empty folder.
                    print "Could not clean up %s.  There are no empty directories." % root

if __name__ == "__main__":
    def menu():
        print "1) Move Files"
        print "2) Perform Album Check"
        print "3) Cleanup a Directory"
        print "4) Exit"
        print
        menuChoice = raw_input("Input Option: ")
    menuChoice = 0
    
    while True:
        amove = AUDIOMover()
        menu()
        if menuChoice == '1':
            source = os.path.normpath(raw_input("Input source folder path: "))
            dest = os.path.normpath(raw_input("Input destination folder path: "))
            delchoice = yesOrNo("Delete old files?")
            amove.fileFind(source)
##            amove.makeNewDir(dest)
            amove.fileMove(dest, delchoice)
            print "%d files were moved from %s to %s" % \
            (len(amove.fileList), source, dest)
            print '\n' * 3
        elif menuChoice == '2':
            root = os.path.normpath(raw_input("Input folder to check albums of: "))
            amove.fileMoveAlbum(root)
            print root + "was resorted by album."
            print '\n' * 3
        elif menuChoice == '3':
            clean = os.path.normpath(raw_input("Input folder to clean up: "))
            amove.folderCleanUp(clean)
            print clean + "was cleaned up."
            print '\n' * 3
        elif menuChoice == '4':
            print "Thank you."
            time.sleep(2.2)
            break
