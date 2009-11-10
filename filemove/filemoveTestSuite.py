# FileFind should find all the files of specified type in the dir tree
# FileMove should move all the files of type in dir tree to dir and organize 
# them according to organization principles.
# DirCleanUp should delete all the empty directories in a dir tree and leave any files alone
# Albumcheck should cross-reference the albums of all the different music files
# in a dir tree to see if any should be in the same folder that aren'tx

# Idea for unit-testing filemover: create a module that mimics filemover's interaction with the os that will
# then log what the program is trying to do to the os.

# Also a possibility that my functions are too complex for unit-testing.  Possibly spec-ing out a new program
# would help fix this.  Start with the basic ideas and try and forget what i've done with the program so far.

# Undo function idea: the original fileObj list has the full pathname of the original location of all the files.
# Undo could then basically be, save old fileList, fileFind in dest, and map the new fileList to the old with a reverse
# shutil.move