import os

def checkDir(dir):
    directories = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if os.path.splitext(file)[1].lower() == '.py':
                directories.append(root)
    for path in directories[:]:
        if not directories.count(path) == 1:
            directories.remove(path)
    return directories

def addDirs(directories):
    try:
        dirfile = open(r"C:\Python26\dirs.pth",'w')
        for folder in directories:
            dirfile.write("{0}\n".format(folder))
    except IOError:
        print "File open failed."
    finally:
        dirfile.close()

if __name__ == "__main__":
    homedir = r"C:\Users\Geoff\prog\py"
    addDirs(checkDir(homedir))
    