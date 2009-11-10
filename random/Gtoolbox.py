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
    while True:
        answer = raw_input(prompt)
        if answer in outputs:
            return answer
        else:
            print "Invalid input, please try again:"

def sanitizePath(fileName):
    """Remove \, / and whitespace from filenames"""
    newpath = fileName.replace("\\", "")
    newpath = newpath.replace("/", "")
    return newpath.replace(".", "")

if __name__ == '__main__':
    print validateInput("Only 5:", '5')
    print yesOrNo()
    print sanitizePath('TH\\is sho/uld be pl.ain and unpunctuated.')