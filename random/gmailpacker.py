import os, shutil

bytesize = 32312340
top = os.path.normpath(raw_input("Dirname?: "))
foldernamelist = [str(i) for i in range(2000)]
filelist = []
filelistsize = 0

for root, dirs, files in os.walk(top):
    for file in files:
        filepath = os.path.join(root, file)
        size = os.path.getsize(filepath)
        if size < bytesize:
            filelist.append(filepath)
            filelistsize = filelistsize + size
        else:
            newfolder = os.path.join(root, foldernamelist.pop(0))
            for file2 in filelist:
                try:
                    os.mkdir(os.path.join(root, newfolder))
                except:pass
                finally:
                    shutil.copyfile(file2, os.path.join(newfolder, os.path.split(file2)[1]))
            filelist = []
            filelistsize = 0