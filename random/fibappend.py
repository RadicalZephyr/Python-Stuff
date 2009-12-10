
def appendNextFib(fibList):
  # PRE: fibList is a list of ordered fibonacci series numbers if the list
  # is empty, it starts the series with 1
  # POST: this returns the next number in the series as well as appending
  # it to the given list
    if fibList:
        if len(fibList) > 1:
          temp = fibList[-1] + fibList[-2]
          fibList.append(temp)
          return temp
        else:
          fibList.append(1)
          return 1
    else:
      fibList.append(0)
      return 0

def main():
  fibSeq = []
  for i in range(20):
    print appendNextFib(fibSeq)

main()
