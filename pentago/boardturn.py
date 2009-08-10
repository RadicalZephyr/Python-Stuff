
def rotate(boardObj, direction):
    lis = boardObj.stones
    getattr(boardturn, direction)(lis)
    # Use getattr plus direction to call the apppropriate turning function 'cw' or 'ccw'



def cw(lis):
    list1 = list(lis)
    lis[2][0] = list1[0][0]
    lis[2][2] = list1[2][0]
    lis[0][2] = list1[2][2]
    lis[0][0] = list1[0][2]

    lis[1][0] = list1[0][1]
    lis[0][1] = list1[1][2]
    lis[1][2] = list1[2][1]
    lis[2][1] = list1[1][0]

def ccw(lis):
    list1 = list(lis)
    lis[2][0] = list1[2][2]
    lis[2][2] = list1[0][2]
    lis[0][2] = list1[0][0]
    lis[0][0] = list1[2][0]

    lis[1][0] = list1[2][1]
    lis[0][1] = list1[1][0]
    lis[1][2] = list1[0][1]
    lis[2][1] = list1[1][2]