"""A Toolbox of different short convenience functions."""

def yesOrNo(prompt):
    """Takes a prompt for a y/n answer"""
    answer = restrictedInput(prompt, 'Y', 'y', 'N', 'n')
    if answer.upper() == 'Y':
        return True
    elif answer.upper() == 'N':
        return False

def restrictedInput(prompt, outputs):
    """Take a prompt and list of acceptable inputs, only returns user's 
       input when they enter something valid"""
    while True:
        answer = raw_input(prompt)
        if answer in outputs:
            return answer
        else:
            print "Invalid input, please try again:"

def sanitizePath(path):
    newpath = path.replace("\\", "")
    newpath = newpath.replace("/", "")
    return newpath.replace(".", "")
    