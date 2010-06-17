"""Dynamic portfolio page builder

Generates a set of related webpages based on the contents of an image folder
"""

import os, sys, hdi
from templategenerator import templateExpand
from hdi2 import addContent
from optparse import OptionParser

# The idea here is to dynamically generate the portfolio pages based on the folders in the
# images folder, except for banners.  So just take the image folder as an argument.
# Then dynamically generate ALL the portfolio pages. Optional param for relative path to image
# folder from main site location

imageformats = [".jpg", ".png", ".gif", ".jpeg"]

def makePage(folderpath, options):
    root, dirs, files = os.walk(folderpath).next()
    root = os.path.split(root)[1]
    htmlstring = """<h3>{0}</h3>
<div id="portfolio">
<ul class="gallery">
<li class="active"><img src="{1}{2}/main.jpg" title="" alt="" /></li>
""".format(root.title(), options.relpath, root)

    for file in files:
        if os.path.splitext(file)[1] in imageformats:
            if not os.path.splitext(file)[0] == "main":
                htmlstring += """<li><img src="{0}{1}/{2}" title="" alt="" /></li>
""".format(options.relpath, root, file)
    htmlstring += "</ul></div>"

    html = addContent(htmlstring, options.content, "content")
    html = addContent(options.menu, html, "submenu")
    
    if root == options.default:
        with open("{0}portfolio.html".format(options.head), 'w') as fpage:
            fpage.write(html)
    else:
        with open("{0}portfolio_{1}.html".format(options.head, root), 'w') as fpage:
            fpage.write(html)

def makeFolderPages(options):
    imageroot = os.path.join(options.head, options.relpath)

    root, dirs, files = os.walk(imageroot).next()
    menuhtml = "<ul>"

    options.default = dirs[0]
    with open(os.path.join(options.head, "porttemp.html")) as template:
        options.content = template.read()

    for dir in dirs:
        if dir == options.default:
            menuhtml += """<li><a href="portfolio.html">{0}</a></li>
""".format(dir.title())
        else:
            menuhtml += """<li><a href="portfolio_{0}.html">{1}</a></li>
""".format(dir.lower(), dir.title())
    menuhtml += "</ul>"
    options.menu = menuhtml

    for dir in dirs:
        makePage(os.path.join(root,dir), options)

def getHead(imagepath, relpath):
    pathcopy = imagepath
    rels = relpath.split('/')
    while os.path.split(pathcopy)[1] not in rels:
        pathcopy = os.path.split(pathcopy)[0]
        
    return os.path.split(pathcopy)[0].replace(os.sep, os.altsep)+'/'

def main():
    parser = OptionParser()
    parser.add_option("-r", "--relative", dest="relpath",
                      default="images/",
                      help="specifiy an alternative relative path\
                      from the html location to the image folder. Default is 'images/'.\
                      Must be a portion of the same path as image folder.",
                      metavar="PATH")
    parser.add_option("-s", "--skip", dest="toSkip",
                      default="",
                      help="specify folder name(s) to skip",
                      metavar="FOLDER[,FOLDER]*")
    
    (options, args) = parser.parse_args()

    options.head = getHead(args[0], options.relpath)

    makeFolderPages(options)
    
if __name__ == "__main__":
    main()