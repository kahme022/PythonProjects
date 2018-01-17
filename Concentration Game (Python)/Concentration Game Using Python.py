import random
import time  # for sleep
       
def shuffle_deck(deck):
    '''(list of str)->None
       Shuffles the given list of strings representing the playing deck    
    '''
    random.shuffle(deck)
    for i in range(2):
    	print ("\r- Shuffling", end='')
    	time.sleep(0.5)
    	print ("\r\ Shuffling", end='')
    	time.sleep(0.5)
    	print ("\r| Shuffling", end='')
    	time.sleep(0.5)
    	print ("\r/ Shuffling", end='')
    print("\rShuffle complete.")

def create_board(size):
    '''int->list of str
       Precondition: size is even positive integer between 2 and 52
       Returns a rigorous deck (i.e. board) of a given size.
    '''
    board = [None]*size 

    letter='A'
    for i in range(len(board)//2):
        board[i]=letter
        board[i+len(board)//2 ]=board[i]
        letter=chr(ord(letter)+1)
    return board

def print_board(a):
    '''(list of str)->None
       Prints the current board in a nicely formated way
    '''
    for i in range(len(a)):
        print('{0:4}'.format(a[i]), end=' ')
    print()
    for i in range(len(a)):
        print('{0:4}'.format(str(i+1)), end=' ')
    print()

def wait_for_player():
    '''()->None
    Pauses the program/game until the player presses enter
    '''
    input("\nPress enter to continue. ")
    print()

def print_revealed(discovered, p1, p2, original_board):
    '''(list of str, int, int, list of str)->None
    Prints the current board with the two new positions (p1 & p2) revealed from the original board
    Preconditions: p1 & p2 must be integers ranging from 1 to the length of the board
    '''
    for i in range(len(original_board)):
        if i == p1 or i == p2:
            print('{0:4}'.format(original_board[i]), end=' ')
        else:
            print(discovered + "   ", end=' ')
    print()
    for i in range(len(original_board)):
        print('{0:4}'.format(str(i+1)), end=' ')
    print()
    

#############################################################################
#   FUNCTIONS FOR OPTION 1 (with the board being read from a given file)    #
#############################################################################

def read_raw_board(file):
    '''str->list of str
    Returns a list of strings represeniting a deck of cards that was stored in a file. 
    The deck may not necessarifly be playable
    '''
    raw_board = open(file).read().splitlines()
    for i in range(len(raw_board)):
        raw_board[i]=raw_board[i].strip()
    return raw_board


def clean_up_board(l):
    '''list of str->list of str

    The functions takes as input a list of strings representing a deck of cards. 
    It returns a new list containing the same cards as l except that
    one of each cards that appears odd number of times in l is removed
    and all the cards with a * on their face sides are removed
    '''
    print("\nRemoving one of each cards that appears odd number of times and removing all stars ...\n")
    playable_board=[]

    # filter '*' cards
    for i in l:
        if i != '*':
            playable_board.append(i)

    counts = histogram(playable_board)

    # determine cards that have an odd count
    removes = []
    for i, j in counts.items():
        if j % 2 == 1:
            removes.append(i)

    # filter odd count cards
    for i in removes:
        playable_board.remove(i)
    
    return playable_board


def is_rigorous(l):
    '''list of str->True or None
    Returns True if every element in the list appears exactlly 2 times or the list is empty.
    Otherwise, it returns False.

    Precondition: Every element in the list appears even number of times
    '''
    counts = histogram(l)
    for i, j in counts.items():
        if j != 2:
            return False

    return True 


####################################################################3

def play_game(board):
    '''(list of str)->None
    Plays a concentration game using the given board
    Precondition: board a list representing a playable deck
    '''

    # this is the funciton that plays the game
    turns = 0
    while len(board) > 0:
        print_revealed("*", -1, -1, board)

        length = len(board)

        first = input("First card number (1 to " + str(length) + "): ")
        try:
            first = int(first) - 1
        except ValueError:
            first = -1
        if first < 0 or first >= length:
            continue

        second = input("Second card number (1 to " + str(length) + "): ")
        try:
            second = int(second) - 1
        except ValueError:
            second = -1
        if second < 0 or second >= length:
            continue

        if first == second:
            continue

        print_revealed(" ", first, second, board)
        if board[first] == board[second]:
            if first > second:
               del board[first]
               del board[second]
            else:
               del board[second]
               del board[first]
        else:
            print ("You missed!")

        turns += 1

    print ("GAME OVER")
    print ("It took you " + str(turns) + " to play.")


# return histogram of a deck
def histogram(deck):
	'''(list of str) -> list of str'''
	result = {}
	uniques = set(deck)
	for i in uniques:
		result[i] = deck.count(i)
	return result


# show main menu
def menu():
	'''(None) -> None'''
	print ("Enter a choice.")
	print ("\t1. Generate a rigorous deck of cards.")
	print ("\t2. Read the deck from a file.")


#main

print ("************************************")
print ("* Welcome to my Concentration game *")
print ("************************************")

choice = 0
while choice < 1 or choice > 2:
	menu()
	choice = input("> ");
	try:
		choice = int(choice)
	except ValueError:
		choice = 0

if choice == 1:
	number = 1
	while number % 2 == 1 or (number < 2 or number > 52):
		number = input("Enter number of cards (even from 2 to 52): ")
		try:
			number = int(number)
		except ValueError:
			number =  1

	board = create_board(number)
	print_board(board)

elif choice == 2:
	file = input("Enter the name of the file: ")
	file = file.strip()
	board = read_raw_board(file)
	board = clean_up_board(board)
	print_board(board)

shuffle_deck(board)
play_game(board)
