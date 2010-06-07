"""3. Write a function using Recursion to enter and display a string in reverse.
Don't use arrays/strings."""

def enterStr(q=-1, z=""):
    if not z:
        z = raw_input("enter str1: ")
    if len(z)==-q:
        print z[q]
        return
    print z[q],
    return enterStr(q-1, z)

#---------------

"""4. Write a function using Recursion to enter and display a string in reverse and state
whether the string contains any spaces. Don't use arrays/strings."""

def multEnterStr(q=-1, c=0, z=""):
    if not z:
        z = raw_input("enter str2: ")
    if len(z)==-q:
        print z[q]
        print "it has %i spaces" %c
        return
    print z[q],
    if z[q]==" ":
        return multEnterStr(q=q-1, c=c+1, z=z)
    else: return multEnterStr(q=q-1, c=c, z=z)

#-----------------------

"""5. Write a function using Recursion to check if a number n is prime. (You have to check whether
n is divisible by any number below n)"""

def primeCheckk(n, z=2):
    if n==z or n==1:
        return "a prime"
    else: 
        if n%z!=0:
            return primeCheckk(n, z+1)
        else:
            return "not a prime"

#-------------------------------

"""6. Write a function using Recursion to enter characters one by one until a space is encountered.
The function should return the depth at which the space was encountered."""

def enterOneByOne(z=None, q=""):
    z=raw_input("enter one letter: ")
    q = q+z
    if z==" ":
        return q, q.index(" ")+1
    else:
        return enterOneByOne(z, q)

if __name__ == "__main__":
    #print enterOneByOne()
    #print primeCheckk(17)
    enterStr()
    multEnterStr()