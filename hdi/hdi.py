# Script for inserting the auto-generated html from open-office into a webpage
# PREconditions: that the webpage have only one div with an id="contentbody"
# and that this is where the modified content needs to go.
# the main function also only takes two arguments, the name of the new content
# file and the name of the real html document in that order. (Local, not full paths)

# Extension notes -- need to be able to close <LI> tags intelligently
# also need to remove <P> tags from the <LI> elements

import re, os, sys, tidy


        

def stripFluff(html):
    """Return a string of html content.
    
    Takes an auto-generated html page and strips out the fluff
    e.g. extra inline styles, extraneous spans etc. and returns
    a well-formed and plain html version.  Only captures stuff
    within the body tag.  """

    options = dict(output_xhtml=1,indent=0,tidy_mark=0,
                   clean=1, drop_empty_paras=1, drop_font_tags=1,
                   drop_proprietary_attributes=1, enclose_block_text=1,
                   literal_attributes=1, logical_emphasis=1, merge_divs=0,
                   error_file='tidyerror.log', gnu_emacs=1, bare=1)
    html = str(tidy.parseString(html, **options))

    pattern = r'<body.*?</body>'

    temp = re.findall(pattern, html, re.DOTALL|re.I)[0]
    temp = removePattern(temp, r'<body.*?>')
    temp = temp.replace('</body>', '')
    #temp = removePattern(temp, r'\r\n')
    temp = cleanLi(temp)
##    temp = removePattern(temp, r'<SPAN.*?>')
##    temp = temp.replace('</SPAN>', '')
##    temp = removePattern(temp, r'<FONT.*?>')
##    temp = temp.replace('</FONT>', '')
    temp = removePattern(temp, r'style=".*?"')
    temp = removePattern(temp, r'target=".*?"')
    temp = removePattern(temp, r'class=".*?"')
    temp = temp.replace('<br>', '<br />')
    temp = lowerTags(temp)
    return temp

def cleanLi(html):
    if type(html) == str:
        pattern = r'<li>.*<p.*?>.*?</p>'
        occurences = re.findall(pattern, html, re.DOTALL|re.I)
        new = html
        for item in occurences:
            temp = removePattern(item, r'<p.*?>')
            temp = removePattern(temp, r'</p>')
            new = new.replace(item, temp)
        return new

def removePattern(html, pattern):
    if type(html) == str:
        occurences = re.findall(pattern, html, re.DOTALL|re.I)
        temp = html
        for item in occurences:
            temp = temp.replace(item, '')
        return temp

def addContent(content, html, id="contentbody", append=False):
    """Inserts content into html after id

    Both arguments are strings.  Id can either be
    an element id string (no '<>' or an html tag
    with '<>'"""
    
    if id[0] == '<' and id[-1] == '>':
        strToFind = id
    else:
        strToFind = 'id="%s">' % id

    if append:
        start = html.find(strToFind)
    else:
        start = html.find(strToFind) + len(strToFind)

    return html[:start] + content + html[start:]
    
def lowerTags(html):
    """Convert only the tags in an html doc to lowercase"""
    pattern = r'<.*?>'
    matches = re.findall(pattern, html, re.DOTALL)
    for item in matches:
        html = html.replace(item, item.lower())
    return html

if __name__ == "__main__":

    contentpath = os.path.join(os.getcwd(), sys.argv[1])
    htmlpath = os.path.join(os.getcwd(), sys.argv[2])

    with open(contentpath) as content:
        with open(htmlpath, 'r+') as html:

            contentstring = stripFluff(content.read())
            htmlstring = html.read()

            if htmlpath.find('content') == -1:
                headername = os.path.splitext(sys.argv[2])[0]
                headername = headername.capitalize() + ' '

                if sys.argv[3] == 'dohead':
                    if headername.lower() != 'index ':

                        htmlstring = addContent(headername, htmlstring, "<title>")
                        htmlstring = addContent(headername, htmlstring, "sectiontitle")
                    else:
                        htmlstring = addContent('Home', htmlstring, "sectiontitle")

                writestring = addContent(contentstring, htmlstring)

            else:
                headername = os.path.splitext(sys.argv[1])[0]
                headername = headername[:headername.find('content')]

                if sys.argv[3] == 'append':
                    htmlstring = addContent(contentstring, htmlstring, "</body>", True)
                else:
                    htmlstring = addContent(contentstring, htmlstring, headername)

                writestring = htmlstring                    
            
            html.seek(0, 0)
            html.write(writestring)

            
