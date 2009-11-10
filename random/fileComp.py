import fileinput, os

def lineComp(file1, file2, output=True):
    """
    A line by line comparison of two files

    output flag sets whether or not to write the
    disparate lines to a new file.
    """

    one = fileinput.FileInput(file1)
    two = fileinput.FileInput(file2)
    

    def nextLine(): return str(one.readline()), str(two.readline())

    count = 0
    
    while count < 299:
        count += 1
        a,b = nextLine()
        if not (output and (a == b)):
            log = open('diflog.txt', 'a')
            log.write(" - ".join([str(one.lineno()),a]))
            log.write("\n")
            log.write(" - ".join([str(two.lineno()),b]))
            log.write("\n\n")
            log.close()

    one.close()
    two.close()

if __name__ == "__main__":
    os.chdir(os.path.normpath(r"D:\Continuum Web Files\BAK files"))
    file1 = os.path.normpath(raw_input("First file to compare: "))
    file2 = os.path.normpath(raw_input("Second file to compare: "))
    lineComp(file1, file2)