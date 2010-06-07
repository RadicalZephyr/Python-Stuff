# hdi rewrite with better script option support and less kludge (hopefully)

import re, os, tidy, sys
from optparse import OptionParser

usage = "usage: %prog [options] source dest insert the body of source html into dest"
    
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
        strToFind = id[:-1] + '.*?>'
    else:
        strToFind = 'id="{0}".*?>'.format(id)
        
    strToFind = append and strToFind + ".*?</" or strToFind

    match = re.search(strToFind, html, re.I)
    if match:
        start = append and (match.end() - 2) or match.end()
    else:
        print "location not found."
        print usage
        sys.exit(2)

    return html[:start] + content + " " + html[start:]
    
def lowerTags(html):
    """Convert only the tags in an html doc to lowercase"""
    pattern = r'<.*?>'
    matches = re.findall(pattern, html, re.DOTALL)
    for item in matches:
        html = html.replace(item, item.lower())
    return html

def openAnything(source):
    import urllib
    try:
        return urllib.urlopen(source)
    except (IOError, OSError):
        pass
    
    try:
        return open(source)
    except (IOError, OSError):
        pass
    
    import StringIO
    return StringIO.StringIO(str(source))

def getContent(filename, options):
    
    try:
        with openAnything(filename) as source:
            return options.clean and stripFluff(source.read()) or source.read()
    except IOError:
        print "file does not exist, or path is incorrect"
        print usage
        sys.exit(2)

def htmlInsert(sourcename, destname, options):
    contentstring = getContent(sourcename, options)

    with open(destname, 'r+') as dest:
        htmlstring = dest.read()

        htmlstring = options.title and addContent(options.title, htmlstring, "<title>") or htmlstring
        htmlstring = options.dohead and addContent(options.dohead, htmlstring, "sectiontitle") or htmlstring

        if options.append:
            htmlstring = addContent(contentstring, htmlstring, options.location, append=True)
        else:
            htmlstring = addContent(contentstring, htmlstring, options.location, append=False)
        dest.seek(0, 0)
        dest.write(htmlstring)
        
def main():
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--clean", action="store_true", dest="clean", default=False,
                      help="cleanup the html of the source file before insertion")
    
    parser.add_option("-d", "--dohead", dest="dohead", metavar="HEADER", default="",
                      help="insert the file name minus extension into the first h1 tag")

    parser.add_option("-t", "--title", dest="title", metavar="title", default="",
                      help="insert the file name minus extension into the title attribute")

    parser.add_option("-l", "--location", dest="location", default="contentbody",
                      help="specify an alternate location to insert content using id, or tagname,\
                      default is 'content'", metavar="SELECTOR")

    parser.add_option("-a", "--append", action="store_true", dest="append",
                      default=False, help="change mode to append content")

    (opts, args) = parser.parse_args()

    if len(args) != 2:
        print usage
        sys.exit(2)

    htmlInsert(args[0], args[1], opts)


if __name__ == "__main__":
    main()