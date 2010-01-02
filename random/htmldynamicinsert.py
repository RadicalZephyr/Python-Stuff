# Script for inserting the auto-generated html from open-office into a webpage
# PREconditions: that the webpage have only one div with an id="contentbody"
# and that this is where the modified content needs to go.
# the main function also only takes two arguments, the name of the new content
# file and the name of the real html document in that order. (Local, not full paths)

import re, os, sys

def stripFluff(html):
    """Return a string of html content.
    
    Takes an auto-generated html page and strips out the fluff
    e.g. extra inline styles, extraneous spans etc. and returns
    a well-formed and plain html version.  Only captures stuff
    within the body tag.  """

    pattern = r'<body>.*?</body>'
    body = re.findall(pattern, html, re.DOTALL)
    print body
    nospans = removePattern(body, r'<span.*?>')
    print type(nospans)
    nospans = nospans.replace('</span>', '')
    nostyles = removePattern(nospans, r'style=".*?"')
    
def removePattern(html, pattern):
    occurences = re.findall(pattern, html, re.DOTALL)
    temp = html
    for item in occurences:
        temp = temp.replace(item, '')
    return temp

def addContent(content, html, id="contentbody"):
    """Inserts content into html after id

    Both arguments are strings"""

    strToFind = '<div id="%s">' % id
    start = html.find(strToFind) + 22
    temp = html
    return temp[:start] + content + temp[start:]
    

if __name__ == "__main__":

    contentpath = os.path.join(os.getcwd(), sys.argv[1])
    htmlpath = os.path.join(os.getcwd(), sys.argv[2])


    with open(contentpath) as content:
        with open(htmlpath, 'a') as html:

            contentstring = stripFluff(content)

            htmlstring = html.read()

            html.seek(0, 0)
            html.write(htmlstring)
