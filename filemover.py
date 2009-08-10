import os
import shutil
from fileinfo_fromdict import *
from os.path import join


def getExtList(ftype):
    if str(ftype).startswith('.'): # If it's a string of a single filetype return a list
        return [ftype]
    elif str(ftype).startswith('['): # If it's a list, return the list
        return ftype
    elif ftype == 'audio':
        return ['.mp2','.mp3','.ogg','.flac','.aac','.wma','.wav']
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
        self.fileDict = {}
        
    def fileFind(self, dir):
        """
        Search through a directory tree looking for the
        filetype this class was instantiated to look for
        """
        for root, dirs, files in os.walk(dir):
            self.fileDict[root] = listDirectory(root, self.extList)

    def makeNewDir(self, dir):
        for root in self.fileDict:
            for fObject in self.fileDict[root]:
                try:
                    os.makedirs(join(dir,self.type))
                except WindowsError:
                    pass
            
class AUDIOMover(fileMover):  # Add functionality for multiple artist album weeding
    "move and organize audio files"  # do this by looping through self.fileDict looking for
    def makeNewDir(self, dir):  # file objs that have same album but different artists
        for root in self.fileDict:
            for fObject in self.fileDict[root]:
                try:
                    os.makedirs(join(dir,fObject.get('artist'),fObject.get('album')))
                except WindowsError:
                    pass

    def fileMove(self, dest):
        for root in self.fileDict:
            for fObject in self.fileDict[root]:
                shutil.move(join(dest,fObject['name']),
                            join(dest,str(fObject.get('artist')),str(fObject.get('album'))))

    def albumCheck(self, dir):
        "Check through moved folders for albums with only one song"
        self.albumList = []
        for root, dirs, files in os.walk(dir):
            fileObs = listDirectory(root, fileExtList)
            if len(fileObs) == 1:
                self.albumList.append(fileObs[0])

if __name__ == "__main__":
    source = os.path.normpath(raw_input("Input source folder path: "))
    dest = os.path.normpath(raw_input("Input destination folder path: "))
    amove = AUDIOMover('audio')
    amove.fileFind(dest)
    amove.makeNewDir(source)
    amove.fileMove(source)