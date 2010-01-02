# Script for taking the template for CG website and generating
# the appropriately named files.

import os, shutil, sys

def templateExpand(template, *names):

    if str(template)[0] == '[':
        names = template[1:]
        template = template[0]
    templateDir = os.path.split(template)[0]
    extension = os.path.splitext(template)[1]
    
    for name in names:
        tempname = name + extension
        print (template, os.path.join(templateDir, tempname))
        shutil.copyfile(template, os.path.join(templateDir, tempname))

if __name__ == '__main__':

    args = sys.argv[1:]
    templateExpand(args)