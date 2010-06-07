"""A Toolbox of different short convenience functions."""

def yesOrNo(prompt="Y/N?"):
    """Takes a prompt for a y/n answer, returns boolean"""
    answer = validateInput(prompt, 'Y', 'y', 'N', 'n')
    if answer.upper() == 'Y':
        return True
    elif answer.upper() == 'N':
        return False

def validateInput(prompt, *outputs):
    """Take a prompt and list of acceptable string inputs, only returns user's 
       input when they enter something valid"""
    outputsList = list(outputs)
    for i in outputs:
        if type(i) == list:
            outputsList.extend(i)
            outputsList.remove(i)

    while True:
        answer = raw_input(prompt)
        if answer in outputsList:
            return answer
        else:
            print "Invalid input, please try again:"

def sanitizePath(fileName):
    """Remove \, / and whitespace from filenames"""
    newpath = fileName.replace("\\", "")
    newpath = newpath.replace("/", "")
    return newpath.replace(".", "")

def typesInList(iterable):
    """Return a list of all the types in a list."""
    typelist = []
    for i in iterable:
        if not type(i) in typelist:
            typelist.append(type(i))

    return typelist

def listIsType(iterable, listtype):
    """Verifies that a list is of type listtype"""
    return listtype in typesInList(iterable)

if __name__ == '__main__':
    print validateInput("Only 5:", '5')
    print yesOrNo()
    print sanitizePath('TH\\is sho/uld be pl.ain and unpunctuated.')
    print typesInList(['a', 1, True, 1, 2.3])
    print listIsType([1,2,4,5], int)