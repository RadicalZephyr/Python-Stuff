# mutagen using filemover program helper functions

def makeOrgList(inputString):
    """Take user input and convert to a list

    Allow for maximum user stupidity, supposed to
    take input in form "toptier nexttier ... last tier"
    outputs a list of ['toptier', 'nexttier', ... 'lasttier']
    can take ' ', ', ', '/', and '\' as delimiters."""
    
    # Hope user can follow instructions
    orgList = inputString.split(' ')
    # But check all the easy ways they could mess up
    if len(orgList) == 1:
        orgList = inputString.split(', ')
    
    if len(orgList) == 1:
        orgList = inputString.split('/')

    if len(orgList) == 1:
        orgList = inputString.split('\\')

    return orgList

def getExtList(ftype):
    ftypeString = str(ftype)
    if ftypeString == 'all':
        return ['.*']
    elif ftypeString.startswith('.'): # If it's a string of a single filetype return a list
        return [ftype]
    elif ftypeString.startswith('['): # If it's a list, return the list
        return ftype
    elif ftype == 'audio':
        return ['.mp2','.mp3', '.m4a', '.ogg','.flac','.aac','.wma','.wav']
    elif ftype == 'video':
        return ['.avi','.divx','.mp4','.ogm','.qt','.wmv','.mov']
    elif ftype == 'text':
        return ['.txt','.doc','.docx','.odt','.rtf']
    elif ftype == 'prog':
        return ['.py','.c','.pl']
    else:
        print >> sys.stderr, "ftype not defined."
