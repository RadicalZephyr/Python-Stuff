from Gtoolbox import *

class MultiArray:
    
    def __init__(self, *args, **kwargs):
        args = list(args)
        self.dimensions = len(args)
        self.size = args
        self.length = 1
        for i in self.size:
            self.length = self.length * i
        
        if not "defval" in kwargs.keys():
            defval = 0
        else:
            defval = kwargs["defval"]

        self.array = self.__buildArray(self.dimensions, args, defval)
        self.accessed = self.__buildArray(self.dimensions, args, False)


    def __buildArray(self, dimension, sizes, defval=0):
        temp = sizes[-dimension]
        if dimension == 1:
            return [defval for i in xrange(temp)]
        elif dimension > 1:
            return [self.__buildArray(dimension-1, sizes) for i in xrange(temp)]

    def __accessValue(self, array, coords, getFlag=True):
        temp = coords.pop(0)
        if len(coords) == 0:
            if getFlag:
                return array[temp]
            else:
                return (array, temp)
        elif len(coords) > 0:
            return self.__accessValue(array[temp], coords)

    def __checkIndex(self, index):
        for i in xrange(len(index)):
            if not index[i] <= self.size[i]:
                return False
        return True

    def __getitem__(self, args):
        if not listIsType(args, int):
            raise TypeError
        if not len(args) == self.dimensions:
            raise IndexError
        elif not self.__checkIndex(args):
            raise IndexError
        else:
            return self.__accessValue(self.array, list(args))

    def __setitem__(self, args, value):
        if not listIsType(args, int):
            raise TypeError
        if not len(args) == self.dimensions:
            raise IndexError
        elif not self.__checkIndex(args):
            raise IndexError
        else:
            temp, key = self.__accessValue(self.array, list(args), getFlag=False)
            print temp
            print key
            print temp[key]
            temp[key] = value

    def __repr__(self):
        return str(self.array)

    def __str__(self):
        if self.dimensions <= 2:
            strRep = ""
            for i in self.array:
                for j in i:
                    strRep = strRep + str(j) + " "
                strRep = strRep + "\n"
            return strRep
        else: return str(self.array)

    def __len__(self):
        return self.length


class Cube(MultiArray):
    def __init__(self, size):
        MultiArray.__init__(size, size, size)

class RubixCube(Cube):
    pass


if __name__ == "__main__":
    ma = MultiArray(3,6, defval=1)
    print ma.array
    print ma[0,1]
    print ma
    print ma.size
    b = [2]
    b[0] = 1
    