import random

EMPTY = "_"                     
X = "X"
O = "O"
TIE = "TIE"
NUM_SQUARES = 9                     
player = X
computer = O

def display_instructions():
    print \
   
def print_board(board):                                                        
    board = [item.replace("_"," ") for item in board]
    print "." + "---." * 3
    for bound in [0,3,6]:
        print "|",
        for sym in board[bound:bound+3]:
            print sym, "|",
        if bound < 6:
            print "\n|" + "---|" * 3
    print "\n'" + "---'" * 3


def asking(question):                            
    response = raw_input("Would you like to go first? (y/n): ").lower()
    while response not in ("y", "n"):                                      
        response = raw_input("Would you like to go first? (y/n): ").lower()
    return response

def number(question, low, high):               
    answer = raw_input("Enter a number between 0-8: ")
    while answer not in right(low, high):
        answer = int(raw_input(question))
    return answer                                             
   
def pieces():
    first = asking("Would you like to go first? (y/n): ")
    if first == "y":
        number = input('\nEnter a number: ')
        player = X
        computer = O
    else:
        print "\nThen I will go first. "
        computer = X
        player = O
    return computer, player

#game = raw_input("Choose yor position: ")
#print_game
def possible_moves(board):                                       

    moves = []
    for square in range(NUM_SQUARES):
        if board[square] == EMPTY:            
            moves.append(square)                               
    return moves                                         

def winner(board):
    Winning_Row = ((0,1,2),(3,4,5),(6,7,8),
                   (0,3,6),(1,4,7),(2,5,8),
                   (0,4,8),(2,4,6))          
    for w in Winning_Row:
        if board[w[0]] == board[w[1]] == board[w[2]] != EMPTY:
            winner = board[w[0]]
            return winner            
        if EMPTY not in board:
            return TIE   
        return None

def player_move(board, player):
   possible = possible_moves(board)
   move = None
   while move not in possible:
       move = int(raw_input("Make your move, 0-8: "))
   return move

def computer_move(board, computer, player):
   board = board[:]
   best_moves = (4, 2, 8, 6, 0, 7, 1, 3)                           
   for move in best_moves:
        if move in possible_moves(board):
            return move


def next_turn(turn):
   if turn == X:
      return O
   else:
      return X


def winner_now(winner, computer, player):
   if winner == player:
      print("You win!")
   elif winner == computer:
         print("Computer win!")
   elif winner == TIE:   
      print("Remi")

def main():                                                   
    display_instructions()
    computer, player = pieces()
    turn = X                                             
    board = ["_","_","_","_","_","_","_","_","_"]
    print_board("".join(board))
    won = winner(board)
    while not won:
        if turn == player:
            move = player_move(board, player)
            board[move] = player
        else:
            move = computer_move(board, computer, player)
            board[move] = computer
        print_board(board)
        turn = next_turn(turn)
        won = winner(board)
        winner_now(winner, computer, player)

main()
raw_input("\n\nPress enter to quit.")      