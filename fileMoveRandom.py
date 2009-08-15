def fileMove(self, dir, delsrc=False, *orgOptions):
    # The goal here is to take a dictionary (or list) of parameters that will inform the program how to organize the file hierarchy.
    # Ex. ["album", "artist"] or ["artist", "album"]
    # One idea is using a list of strings that are then referenced in calls to self.get(listItem)
    # possibly use a for loop? list comprehension seems ungood... unless combined with string concatenation...
##  orgList = [self.get(param) for param in orgOptions]
    # or how about, there's no need for anything except the damn list.  Just pop from the front in the long join call
    # but what about calling that list multiple times? bah...
##    for fObject in self.fileList:
##            try:
##                
##            except WindowsError:
##                pass
    for fObject in self.fileList:
            try: move(fObject['name'],
                      join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
            except IOError:
                try: os.makedirs(join(dir,str(fObject.get('artist')),str(fObject.get('album'))))
                except WindowsError: pass
                move(fObject['name'],
                      join(dir,str(fObject.get('artist')),str(fObject.get('album'))))

# The below block is another possibilty, a self-referential looping join statement to use the whole list given (avoids the potential problem
# of getting too many or too few parameters
# Should look up example usages of optional parameter function handling...
for x in range(-1, -len(orgOptions), -1):
    	str = join(str, orgOptions[x])


self["album"] = self.get("TALB")
self["title"] = self.get("TIT2")
self["artist"] = self.get("TPE1") or self.get("TPE2")
self["tracknum"] = self.get("TRCK")
