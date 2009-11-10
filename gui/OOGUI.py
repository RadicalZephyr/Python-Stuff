import sys
import os

# title used for the application
_TITLE = "Object-Oriented GUI Example"


# command line options description
# (starts up the Tkinter gui unless alternate gui library is specified)
_TKINTER  = 'T'
_WXWIN    = 'W'
_PYQT     = 'Q'
_PYGTK    = 'G'
_FXPY     = 'F'
_GUITYPES = [_TKINTER, _WXWIN, _PYQT, _PYGTK, _FXPY]
# other options with arguments
_GEOMETRY = 'g'
_RESFILE  = 'r'
_STARTDIR = 's'
_OTHEROPT = {_GEOMETRY : 'geometry, e.g., <width>x<height>+<x>+<y>',
             _RESFILE  : 'resourceFile',
             _STARTDIR : 'startupDirectory'}
_HELP     = 'h'


# extensions of filenames the GUI's may know how to handle
_IMAGES   = ("gif", "jpg", "jpeg", "ppm", "bmp", "png", "tif", "tiff", "wmf",
             "pbm", "pil")
_HTML     = ("htm", "html")
_BINARY   = ("pyc", "exe", "o", "obj", "com", "ppt", "doc")

# CHANGE since submitted to Python10
#
# shared GUI config values
APP_HEIGHT     = 500
BORDER         = 10
DISPLAY_WIDTH  = 360
DISPLAY_HEIGHT = 160
DISPLAY_LABEL  = 'Display file: '
DISPLAY_UNAVAIL= 'Viewer Not Available for File'
SASH_MIN       = 100
SASH_POSITION  = 200
DIRS_LABEL     = 'Directories'
FILES_LABEL    = 'Files'
FILENAME_LABEL = 'Selected File'


def _getText(filename):
    """Returns the text of the specified filename, and an 'isBinary' flag
    set to true if the text contains a NULL character
    """
    file = open(filename)
    text = file.read()
    file.close()
    isBinary = text.find(chr(0)) >= 0

    return text, isBinary


def _getFileType(filename):
    """Get the extension of the filename, lower-case it, and strip off '.'"""
    return os.path.splitext(filename)[1].lower()[1:]


class OOGui:
    """Wrapper class for the object-oriented version of the filegui example,
    with the feature of being able to display the selected file.
    """
    def __init__(self, topLevel=None, geometry=None,
                 resourceFile=None, startdir=os.getcwd()):
        """Creates the object-oriented filegui object"""
        # initialize the instance members each derivation sets in buildGUI()
        self._display   = None     # handle to display frame
        self._gotoEntry = None     # text entry for full pathname of directory
        self._dirList   = None     # list of directories
        self._fileList  = None     # list of filename entries
        self._filename  = None     # text entry for full pathname of file
        self._selectedFile = None  # user entered name vs. selected file

        # if the top level window is not passed in, use specialized method
        self._topLevel = topLevel
        if not topLevel:
            self._topLevel = self._getTopLevel()
            
        if not self._topLevel:
            print >> sys.stderr, "Error: No top level window ... aborting ..."
            return
            
        # load the resources (options) for all the 'named' widgets
        if not self._loadResources(resourceFile):
            print "Error loading resources ... continuing..."

        # CHANGE since submission to Python10
        #
        # Use reflection and dynamic binding to include the
        # actual object's derived type name in the title
        title = "%s: %s" % (_TITLE, self.__class__.__name__)

        # build the gui using specialized GUI class method
        self._buildGui(title)

        # CHANGE since submission to Python10
        #
        # initialize our startup directory as specified, default to current dir
        if not startdir:
            startdir = os.getcwd()
        self._setCWD(startdir)

        # run the application
        self._startGui(geometry)


    def _buildGui(self, title):
        """Abstract method to build the GUI."""
        raise NotImplementedError, "Must implement method to build the GUI!"


    def _getCurrentDirectory(self):
        """Abstract method that returns the full pathname of the
        current working directory.
        """
        raise NotImplementedError, \
              "Must implement method that returns the full pathname of the " \
              "current working directory."

        
    def _getSelectedFile(self):
        """Abstract method that returns the basename of the selected entry
        in the files list.
        """
        raise NotImplementedError, \
              "Must implement method that returns the basename of the " \
              "selected entry in the files list."

        
    def _getSelectedDirectory(self):
        """Abstract method that returns the basename of the selected entry
        in the directories list.
        """
        raise NotImplementedError, \
              "Must implement method that returns the basename of the " \
              "selected entry in the directories list."

        
    def _getTopLevel(self):
        """Abstract method used to get the top level (root) window for
        the application.  If the top level window cannot be created
        before constructing the OOGui base, this method is called
        by the OOGui constructor to ensure a valid top level window is
        available upon which to build the GUI.
        """
        raise NotImplementedError


    def _loadResources(self, resourceFile=None):
        """Loads GUI resources to customize the look and feel of widgets;
        return true if all is well. If resource file is used, implementation
        should override method and return value indicating status of load.
        """
        return 1


    def _startGui(self, geometry=None):
        """Abstract method to start the GUI, including the main event loop."""
        raise NotImplementedError, \
              "Must implement method to start the GUI, including " \
              "the main event loop."


    def _displayBinary(self, filename):
        """Abstract method to display binary files with appropriate binary
        viewer.
        """
        raise NotImplementedError, \
              "Must implement method to display binary data files."

        
    def _displayHTML(self, filename):
        """Abstract method to display HTML files."""
        raise NotImplementedError, \
              "Must implement method to display HTML files."

        
    def _displayImage(self, filename):
        """Abstract method to display image files."""
        raise NotImplementedError, \
              "Must implement method to display image files."

        
    def _displayText(self, filename):
        """Abstract method to display text files."""
        raise NotImplementedError, \
              "Must implement method to display text files."


    # CHANGE since submission to Python10
    def _setCWD(self, pathname):
        """Abstract method to set the current working directory to
        'pathname' and update the GUI.
        """
        raise NotImplementedError, \
              "Must implement method to set the current " \
              "working directory to 'pathname' and update the GUI."


    def _setFilename(self, filename):
        """Abstract to set the filename entry text field of the GUI."""
        raise NotImplementedError, \
              "Must implement method to set the filename " \
              "entry text field to 'filename'."
    

    # CHANGE since submission to Python10 (new hook after refactoring)
    def _directorySelected(self, *unused):
        """The base class does the parsing of the selected directory, and
        then calls the derived object's _setCWD() method to set the
        new working directory. Derived GUI classes should NOT implement
        this method; they should call it as the action event handler
        when a directory entry is 'double-clicked'.
        """
        selectedDirectory = self._getSelectedDirectory()
        cwd = self._getCurrentDirectory()

        # remove end separator since we will join with one later, but
        # make sure we're not at the root level already
        if cwd.endswith(os.sep) and (cwd != os.sep):
            cwd = cwd[:-1]

        # do nothing if we get nothing
        if not selectedDirectory or not cwd:
            return

        if selectedDirectory == os.pardir:
            cwd = os.path.dirname(cwd)
        else:
            cwd = os.path.join(cwd, selectedDirectory)
        self._setCWD(cwd)


    def _fileSelected(self, *unused):
        """The base class does the parsing of the selected file, and
        then calls the appropriate display handler for the type of file,
        based on its file extension.  Derived GUI classes should NOT implement
        this method; they should call it as the action event handler when a
        file entry is 'double-clicked'.
        """
        selectedFile = self._getSelectedFile()
        if not selectedFile:
            return

        filename = os.path.join(self._getCurrentDirectory(), selectedFile)
        ext = _getFileType(filename)
        
        # CHANGE since submission to Python10
        # handle file differently if it is a directory
        if os.path.isdir(filename):
            self._setCWD(filename)
            return
        
        # make sure the file exists before delegating
        if not os.access(filename, os.R_OK):
            print >> sys.stderr, "Error reading file: ", filename
            return

        # set the filename entry and then display the file according to its ext
        # (not the UNIX way, mind you, but the easiest for a tutorial :)
        self._setFilename(filename)
        if   ext in _IMAGES:
            self._displayImage(filename)
        elif ext in _HTML:
            self._displayHTML(filename)
        elif ext in _BINARY:
            self._displayBinary(filename)
        else:
            self._displayText(filename)


    # CHANGE since submission to Python10
    #
    def _getEntries(self, cwd):
        """Given the current working directory, returns the names of the
        directory and file entries. (Note: NOT meant to be overridden.)
        """
        files = []
        dirs  = []
        for e in os.listdir(cwd):
            if os.path.isdir(os.path.join(cwd, e)):
                dirs.append(e)
            else:
                files.append(e)

        # sort the lists
        dirs.sort()
        files.sort()
        dirs.insert(0, os.pardir)  # always include the parent directory

        return dirs, files


# -------------------------------------------------------------------------
# Abstract class TO BE used to display the selected file in the OOGui
# implementations.  LEFT AS AN EXERCISE FOR THE STUDENT to refactor
# the current OOGui derived class's frames to use the new impl's.
# -------------------------------------------------------------------------
class DisplayFrame:
    """Abstract class intended to be derived by the different GUI
    toolkits in the tutorial, used to display the selected file in
    the toolkit's OOGui implementation.

    LEFT AS AN EXERCISE FOR THE STUDENT to refactor the current OOGui
    implementations' display frames to use this abstract base class.
    """
    def __init__(self):
        self._sw = None

    def show(self, filename):
        """Figure out what type of file is specified by its extension,
        and then display appropriately using the derived class's
        implementation of the abstract methods.
        """
        if os.path.isdir(filename):
            return
        
        # make sure the file exists before delegating
        if not os.access(filename, os.R_OK):
            print >> sys.stderr, "Error opening file: ", filename
            return
        
        # display the file according to its 'type' (file extension)
        # (not the UNIX way, mind you, but the easiest for a tutorial :)
        ext = _getFileType(filename)
        if   ext in _IMAGES:
            self.image(filename)
        elif ext in _HTML:
            self.html(filename)
        elif ext in _BINARY:
            self.binary(filename)
        else:
            self.text(filename)


    def binary(self, filename):
        """Abstract method to display the binary file named by filename"""
        raise NotImplementedError

    def html(self, filename):
        """Abstract method to display the HTML file named by filename"""
        raise NotImplementedError

    def image(self, filename):
        """Abstract method to display the image file named by filename"""
        raise NotImplementedError

    def text(self, filename):
        """Abstract method to display the text file named by filename"""
        raise NotImplementedError

        

# ----------------------------------------------------------------------
# where it all begins!!
# ----------------------------------------------------------------------
def main(guiType = _TKINTER):
    """The starting point for launching the different GUIs"""
    def usage(msg, error=1):
        """Usage error message for running oogui"""
        if error:
            print >> sys.stderr, 'Error: '
        print >> sys.stderr, msg
        
        # build the option string from our list of supported GUI types
        optstr = ' [-%s] ' % '|'.join(_GUITYPES)

        # add the other supported command line options
        optstr += ''.join(['[-%s %s] ' % (k, v) for k, v in _OTHEROPT.items()])

        print >> sys.stderr, "Usage: %s %s " % (sys.argv[0], optstr)
        print >> sys.stderr, "NOTE: Python 2.0+ is required."
        sys.exit(1)


    # TODO: bring up a launcher instead of command line options for
    # choosing gui library, using multiple threads for different event loops
    #
    # options on command line determine which GUI library to view
    import getopt
    try:
        otherOpts = ''.join([i+':' for i in _OTHEROPT.keys()])
        optstr = '%s%s%s' % (''.join(_GUITYPES), _HELP, otherOpts)
        # use '_' for unused variable name by convention
        args, _ = getopt.getopt(sys.argv[1:], optstr)
    except getopt.GetoptError, detail:
        usage(detail)   # exits the application
        
    geometry = None
    resfile  = None
    startdir = os.getcwd()
    guitype  = guiType

    for arg in args:
        opt = arg[0][1]
        if   opt == _GEOMETRY:
            geometry = arg[1]
        elif opt == _RESFILE:
            resfile  = arg[1]
        elif opt == _STARTDIR:
            startdir = arg[1]
        elif opt.upper() in _GUITYPES:
            guitype = opt.upper()
        elif opt == _HELP:
            usage(__doc__, 0)
        else:
            usage('Unknown option: ' + arg[0])

    args = (geometry, resfile, startdir)
    # launch the requested gui type
    if   guitype == _TKINTER:
        import tkinterGui
        tkinterGui.TkinterGui(*args)
    elif guitype == _WXWIN:
        import wxGui
        wxGui.WxGui(*args)
    elif guitype == _PYQT:
        import pyqtGui
        pyqtGui.PyQtGui(sys.argv, *args)
    elif guitype == _PYGTK:
        import pygtkGui
        pygtkGui.PyGtkGui(sys.argv, *args)
    elif guitype == _FXPY:
        import fxpyGui
        fxpyGui.FxPyGui(sys.argv, *args)
    else:
        print "Unknown option for specifying GUI type: ", guitype


# This idiom allows you to treat more than one python module (file) in
# your application as your runtime 'main' (commonly used for unit testing),
# similar to having each Java module (file) have its own main() method.
#
# Also similar to (in C/C++):
#     #ifdef TEST
#       int main(int argc, char *argv[]) { ... }
#     #endif
#
if __name__ == "__main__":
    """Only gets executed when we run this module"""
    main()