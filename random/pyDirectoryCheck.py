import os

def checkDir(dir):
    directories = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if os.path.splitext(file)[1].lower() == ('.py' or '.pyw'):
                directories.append(root)
    for path in directories[:]: # The funny syntax is to iterate over a copy of the list
        if not directories.count(path) == 1: # instead of the list we're modifying by
            directories.remove(path)    # implicitly making a copy.
    return directories

def addDirs(directories):
    with open(r"C:\Python26\dirs.pth",'w') as dirfile:
        for folder in directories:
            dirfile.write("{0}\n".format(folder))


if __name__ == "__main__":
    homedir = r"C:\Users\Geoff\prog\py"
    addDirs(checkDir(homedir))
    