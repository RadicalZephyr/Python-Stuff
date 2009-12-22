# FileFind should find all the files of specified type in the dir tree
# FileMove should move all the files of type in dir tree to dir and
# organize them according to organization principles.  DirCleanUp
# should delete all the empty directories in a dir tree and leave any
# files alone Albumcheck should cross-reference the albums of all the
# different music files in a dir tree to see if any should be in the
# same folder that aren'tx

# Idea for unit-testing filemover: create a module that mimics
# filemover's interaction with the os that will then log what the
# program is trying to do to the os.

# Also a possibility that my functions are too complex for
# unit-testing.  Possibly spec-ing out a new program would help fix
# this.  Start with the basic ideas and try and forget what i've done
# with the program so far.

# Undo function idea: the original fileObj list has the full pathname
# of the original location of all the files.  Undo could then
# basically be, save old fileList, fileFind in dest, and map the new
# fileList to the old with a reverse shutil.move


# audiocompare and doubleCheck need more work. Right now double doesn't
# return anything, and the test doesn't check that it does anything except
# not fail.
"""Unit test for filemover_mutagen.py"""

import unittest
import filemover_mutagen as fmove

class ClassChecker(unittest.TestCase):
    testFiles = [r"D:\test\a.mp3", r"D:\test\b.mp3", r"D:\test\pdf.pdf",
                 r"D:\test\text.txt"]

    def testFileInfo(self):
        """FileInfo should work with any filetype"""
        for file in self.testFiles:
            fDict = fmove.FileInfo(file)
            self.assertEqual(fDict['name'], file)

    def testID3FileInfo(self):
        """ID3FileInfo should always succeed with files with id3 tags"""
        for file in self.testFiles[0:2]:
            fObject = fmove.ID3FileInfo(file)

    def testID3FileInfoBadFile(self):
        """ID3FileInfo should always fail with files with no id3 tags"""
        for file in self.testFiles[3:-1]:
            self.assertRaises(id3.ID3NoHeaderError, fmove.ID3FileInfo, file)

    def testID3Keys(self):
        """ID3FileInfo should contain certain keys post-initialization"""
        for file in self.testFiles[0:2]:
            fileObj = fmove.ID3FileInfo(file)
            fileObj['album']
            fileObj['title']
            fileObj['artist']
            fileObj['name']

class fileMoveChecks(unittest.TestCase):
    testFiles = [r"D:\test\a.mp3", r"D:\test\b.mp3", r"D:\test\pdf.pdf",
                 r"D:\test\text.txt"]

    def setUp(self):
        self.fileFinder = fmove.fileMover()

    def tearDown(self):
        del self.fileFinder

    def testCanFindAnyFile(self):
        """fileMover should be able to see all the files in the test folder"""
        fileNames = []
        for fDict in self.fileFinder.fileList:
            fileNames.append(fDict['name'])
        for file in fileNames:
            self.assert_(file in self.testFiles)

    def testFileMove(self):
        """fileMover should move all the files"""
        pass

class audioMoveChecks(unittest.TestCase):

    def setUp(self):
        self.amove = fmove.AUDIOMover()

    def tearDown(self):
        del self.amove

    def testDoubleCheck(self):
        """DoubleCheck should run without errors"""
        double = self.amove.doubleCheck(r'D:\test')
        

    def testAudioCompare(self):
        """AudioCompare should find the two test files to be the same"""
        dupes = (r'D:\test\c.mp3', r'D:\test\d.mp3')
        files = (fmove.MP3FileInfo(dupes[0]), fmove.MP3FileInfo(dupes[1]))
        self.assert_(self.amove.audioCompare(files[0], files[1]))
        

if __name__ == "__main__":
    unittest.main()
