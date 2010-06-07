  # Tic Tac Toe
import random

Board = ["1","2","3","4","5","6","7","8","9"]                                 

def playboard():
    for rx in xrange(0,3):
        r = rx * 3
        print '| %s | %s | %s |' %(Board[r+0],Board[r+1],Board[r+2])               
    print

def Win():
    a,b,c,d,e,f,g,h,i = Board 
    winlist = [(a,b,c), (d,e,f), (g,h,i), (a,d,g,), (b,e,h), (c,f,i),               
               (a,e,i), (g,e,c)]
    for w in winlist:
        if w[0]==w[1]==w[2]:                                             
            return True
    return False

playerwin = False            
Run = True
while Run:
    playboard()

    choice = True
    while choice:
        play = raw_input("Make a move, 1-9: ")
        if play.lower() in ["quit","exit","close","end"]:
            choice = Run = False

        try:
            play = int(play)
            if int(Board[play-1]) == play:                                 
                Board[play-1] = "X"
                choice = False
        except:
            pass
        
    
    if Win():                                                      
        playerwin = True
        playboard()
        print "You Win!"
        Run = False

    if all([i in ['X','O'] for i in Board]):
        print "Cat's Game!"
        playerwin = True
        Run = False

    #Computer Turn
    if playerwin == False:
        Moves = []
        for n in xrange(0,9):
            if Board[n] == str(n+1):
                Moves.append(str(n))

        X = random.randint(0,len(Moves)-1)
        X = Moves[X]
        Board[int(X)] = "O"

        if Win():                                                   
            playboard()
            print "Computer Win!"
            Run = False          