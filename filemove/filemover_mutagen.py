# What's next: implement a file cleanup that finds files with identical tags, and deletes or at least finds one copy.
# have a folder clean that finds similarly tagged files and deletes one  on
# the basis of bitrate
# Also have one that makes a list of filename's/paths of low bitrate songs.


import os, sys, shutil, time, id3, mutagen, mp4, flac
from os.path import join
from Gtoolbox import *
from filemoverhelper import *

# This is from Mark Pilgrim's Diveintopython
class FileInfo(dict):
    """store file metadata"""
    def __init__(self, filename=None):
        fileinfo = mutagen.File(filename)
        if fileinfo:
            self = fileinfo
        self["name"] = filename

def listDirectory(directory, fileExtList):
    """Get list of file info objects for files of particular extensions"""
    fileList = [os.path.normcase(f) for f in os.listdir(directory)]
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]
    def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):
        """Get file info class from filename extension"""
        subclass = "{0}FileInfo".format(os.path.splitext(filename)[1].upper()[1:])
        return hasattr(module, subclass) and getattr(module, subclass) \
               or FileInfo
    return [getFileInfoClass(f)(f) for f in fileList]

# From here down is my own work.
class ID3FileInfo(id3.ID3):
    """Functional wrapper for id3.ID3

    Provides the information from id3 tags in an easy to access format
    through the keys album, title, artist, and tracknumber.  Could be extended
    to provide other id3 tag info."""
    def __init__(self, *args, **kwargs):
        try:
            super(ID3FileInfo, self).__init__(*args, **kwargs)
            self["name"] = args[0]
            self["album"] = sanitizePath(str(self.get("TALB")))
            self["title"] = sanitizePath(str(self.get("TIT2")))
            self["artist"] = sanitizePath(str(self.get("TPE1") or self.get("TPE2")))
            self["tracknumber"] = sanitizePath(str(self.get("TRCK")))
        except:
            pass

class MP3FileInfo(ID3FileInfo):
    """Wrapper class for ID3FileInfo to interact with listDirectory"""
    pass

class M4AFileInfo(mp4.MP4):
    """Wrapper class for mutagen.mp4.MP4 to interact with listDirectory"""
    def __init__(self, *args, **kwargs):
        try:
            super(mp4.MP4, self).__init__(*args, **kwargs)
            self["name"] = args[0]
            self["album"] = self['\xa9alb']
            self["title"] = self['\xa9nam']
            self["artist"] = self['\xa9ART'] or self['aART']
            self["tracknumber"] = self['trkn'][0]
        except:
            pass

class MP4FileInfo(M4AFileInfo):
    """Wrapper class for mutagen.mp4.MP4 to interact with listDirectory"""
    pass

class OGGFileInfo():
    """Dispatcher class for figuring out what type of ogg the file is"""
    def __init__(self, file):
        try:
            from oggvorbis import OggVorbis
            self = OggVorbis(file)
            return
        except OggVorbisHeaderError:
            pass
        try:
            from oggspeex import OggSpeex
            self = OggSpeex(file)
            return
        except OggSpeexHeaderError:
            pass
        try:
            from oggflac import OggFLAC
            self = OggFLAC(file)
            return
        except OggFLACHeaderError:
            pass
        try:
            from oggtheora import OggTheora
            self = OggTheora(file)
            return
        except OggTheoraHeaderError:
            pass
        from ogg import OggFileInfo
        self = OggFileInfo(file)
        self["name"] = file
        

class FLACFileInfo(flac.FLAC):
    """Wrapper class for mutagen.flac.FLAC to interact with listDirectory"""
    def __init(self, *args, **kwargs):
        try:
            super(flac.FLAC, self).__init__(*args, **kwargs)
            self["name"] = args[0]
        except:
            pass

class fileMover:
    """Provides basic file moving capabilities for files of ftype

    More advanced capabilities and options can be obtained using the
    child classes, AUDIOMover etc."""

    def __init__(self, ftype='all'):
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

    def fileMove(self, dir):
        """Move files in self.fileList to dir"""
        for fObject in self.fileList:
            try: os.makedirs(join(dir, self.type))
            except: pass
            shutil.move(fObject['name'], dir)

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

    def delFiles(self, fileList=None):
        """Delete all the files in fileList"""

        if not fileList:
            fileList = self.fileList

        for item in fileList:
            os.remove(item["name"])
            
class AUDIOMover(fileMover):
    "move and organize audio files" 
    def __init__(self, ftype='audio'):
        fileMover.__init__(self, ftype)

    def fileMove(self, dir, delsrc=False, fileList=None, organization=["artist", "album"]):
        """Move files in fileList to dir"""
        self.delsrc = delsrc # Record for undo option.
        self.lastDest = dir
        
        move = delsrc and shutil.move or shutil.copy # Check delsrc flag
        if not fileList:    # See if there was another fileList given
            fileList = self.fileList    # if not, use the default

        for fObject in fileList:
            dir = self.lastDest
            for item in organization:    # Build the directory string
                                         # recursively
                dir = join(dir, fObject.get(item, item))
                
            fObject['undoInfo'] = (join(dir, os.path.split(fObject['name'])[1]), \
                                       fObject['name']) # Record for easing undo

# This should be better than the above commented out code
            try: os.makedirs(dir)   # Try to make the new directories
            except WindowsError: pass
            move(fObject['name'], dir) # Do the actual moving
            # End fileMove

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

    def audioEquality(self, fOne, fTwo, flagNum=3):
        """Compare two audio files

        True if they're within a given margin of similarity"""        
        flags = 0
        for val in fOne.keys():
            if fOne[val] == fTwo.get(val):
                flags = flags + 1

        sizeOne = os.path.getsize(fOne['name'])
        sizeTwo = os.path.getsize(fTwo['name'])
        if sizeOne-10 < sizeTwo < sizeOne+10:
            # This should mean if sizeone is within twenty of sizetwo
            # no promises though...
            flags = flags + 1
            
        if flags > flagNum:
            # Arbitrary number of matching file attributes
            return True
        else: return False

    def doubleCheck(self, dir):
        """Check a directory for duplicate files"""

        self.fileFind(dir)
        doubleDict = {}
        for first in self.fileList: # First, get a file from the list
            doubleDict[first] = []  # Make a list to hold all the possibly
                                    # doubles
            for iter in self.fileList:  # Then check all the other files
                if self.audioEquality(main, iter):  # for doubleness
                    doubleDict[main].append(iter)   # add to list if doubled.
        doubleList = []
        for key, value in doubleDict.items():
            if value:
                doubleList.append(key)
                doubleList.extend(value)

        return doubleList
    
        # At this point we have a dictionary of lists, some of which are empty
        # the next step is to throw out the empty lists, and then put the
        # items in the full lists into self.fileList form so it can be passed to
        # fileMove.  Then, filemove should get called so as to put all the
        # duplicates in their own heading under Duplicates

    def undoMove(self):
        """Undo the last fileMove operation."""

        if not self.delsrc: # If the originals weren't deleted, don't try and move
            delSongs(self.lastDest)   # just clean up the dest folder.
        else:
            for fObject in self.fileList:   # Otherwise, reverse the move.
                    shutil.move(fObject["undoInfo"])

    def pprint(self, filelist=None):
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

if __name__ == "__main__":
    def menu():
        print "1) Move Files"
        print "2) Perform Album Check/Sort"
        print "3) Cleanup a Directory"
        print "4) Delete a Directory"
        print "5) Undo Last Operation"
        print "6) Exit"
        print
        global menuChoice
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
            delete = os.path.normpath(raw_input("Input folder to delete: "))
            amove.fileCleanUp(delete)
            amove.folderCleanUp(delete)
            print delete + "was completely removed.  Hope you didn't need anything in there..."
            print '\n' * 3
        elif menuChoice == '5':
            reallyUndo = yesOrNo("Are you sure you want to undo the last file move?")
            if reallyUndo:
                amove.undoMove()
            print "Last move operation undone.  Don't ask for another though..."
            print '\n' * 3
        elif menuChoice == '6':
            print "Thank you."
            time.sleep(2.2)
            break
