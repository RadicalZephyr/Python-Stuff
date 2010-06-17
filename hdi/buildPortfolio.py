"""Dynamic portfolio page builder

Generates a set of related webpages based on the contents of an image folder
"""

import os, sys, hdi
from templategenerator import templateExpand
from optparse import OptionParser

# The idea here is to dynamically generate the portfolio pages based on the folders in the
# images folder, except for banners.  So just take the image folder as an argument.
# Then dynamically generate ALL the portfolio pages. Optional param for relative path to image
# folder from main site location

imageformats = [".jpg", ".png", ".gif", ".jpeg"]

def makeFolderPage(folderpath, options):
    root, dirs, files = os.walk(folderpath).next()
    root = os.path.split(root)[1]

    htmlstring = """<body><div id="projectDetails"><p><a href="#description">Project Details</a></p>
    <div id="description"></div></div>
    <div id="navbar">






    for file in files:
        if os.path.splitext(file)[1] in imageformats:
            htmlstring = htmlstring + """<a href="{0}{1}/{2}" rel="enlargeimage::mouseover" rev="loadarea">
        <img src="{0}{1}/{2}" alt="" width="75px" height="67px" /></a>""".format(options.relpath, root, file)


    htmlstring = htmlstring + """</div>
  <div id="loadarea"><img src="{0}{1}/main.jpg" alt="" name="main" alt="Continuum Gardens" />
  </div></body>""".format(options.relpath, root)
=======
    htmlstring = htmlstring + """</div><div id="outload">
  <div id="loadarea"><img src="{0}{1}/main.jpg" alt="" name="main" alt="Continuum Gardens" />
  </div></div></body>""".format(options.relpath, root)
>>>>>>> origin/master

    with open("{0}{1}content.html".format(options.head, root), 'w') as fpage:
        fpage.write(htmlstring)

    # Now we make a template copy and insert the content we just created into it.
    templateExpand(os.path.join(options.head, 'template.html'), root)
    os.system('python "C:\Users\Geoff\prog\py\projects\hdi\hdi2.py" -t{0} {0}content.html {0}.html'.format(root))

def makeMainPortfolio(imagefolder, options):
    imageroot = os.path.normpath(imagefolder)
    root, dirs, files = os.walk(imageroot).next()
    htmlstring = "<body><ul id=\"plist\">"
    for folder in dirs:
        if not folder in options.toSkip:
            htmlstring = htmlstring + """<li><span><a href="{0}.html"><span class="plink"><img src="{1}{0}/main.jpg"
            alt="{0} Portfolio" width="67px" height="71px" /></span><br />{0}</a></span></li>
        """.format(folder, options.relpath)
            makeFolderPage(os.path.join(root, folder), options)
            print "wrote", folder

    htmlstring = htmlstring + '</ul></body>'
    with open("{0}portfoliocontent.html".format(options.head), 'w') as mainpage:
        mainpage.write(htmlstring)
        print "wrote content"
        
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

    makeMainPortfolio(args[0], options)
    
if __name__ == "__main__":
    main()
    
