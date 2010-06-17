# hdi helper functions


emptyTags = [ '<br>', '<img>', 

class Stack(list):
    def push(self, item):
        self.append(item)

    def top(self):
        temp = self.pop()
        self.push(temp)
        return temp

    def isempty(self):
        return not len(self)

class TagError(Exception):
    pass

def closeTag():
    pass

def getTag(html):
    if not type(html) == str:
        raise TypeError
    return html[:html.find('>')+1]

def isSelfClosing(tag):
    if not type(html) == str:
        raise TypeError
    return tag.endswith(' />')

def isEndTag(tag):
    if not type(html) == str:
        raise TypeError
    return tag.startswith('</')

def stripTag(tag):
    if not type(html) == str:
        raise TypeError
    newtag = ''
    for c in tag:
        if c == ' ':
            break
        else:
            newtag = newtag + c
    return newtag + '>'
    

def parseHtml(html):
    if not type(html) == str:
        raise TypeError
    TagStack = Stack()
    index = 0
    
    while True:
        c = html[index]
        if c == '<':
            tag = getTag(html[index:])
            if isEndTag(tag):
                tag.replace('</', '<')
                if TagStack.top() == tag:
                    TagStack.pop()
                else:
                    raise TagError
                
            elif not isSelfClosing(tag):
                TagStack.push(stripTag(tag))
        if c == len(html):
            break

def handleTagError(tag, index, html):
    if tag in emptyTags:
        
    
            
            