# Description: Two-player abstract board game called Focus/Domination, where the first player to capture
#               6 pieces of the opposing player wins.  Players capture a piece when there are more than 5 pieces
#               on a stack and the bottom piece belongs to the opponent.
#               Players can make moves vertically or horizontally but not diagonally.  Players can make moves with
#               multiple pieces, and can play pieces from the player's own reserve.

class FocusGame:
    """FocusGame allows two players to play an abstract game called Focus/Domination, where they can make moves
    or multiple moves vertically or horizontally, to capture pieces, or place pieces from their reserve."""

    def __init__(self, player1, player2):
        """Instantiate two players.  Initialize both player's reserve and captured as 0, and set first move as None
        and initial turn as None.  Place pieces on board in initial state in pattern according to the game."""
        self._player1 = player1
        self._player2 = player2
        self._player1_reserve = 0
        self._player2_reserve = 0
        self._player1_captured = 0
        self._player2_captured = 0
        self.firstMove = None
        self.turn = None
        self._board = [
            [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
            [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
            [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
            [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
            [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
            [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
        ]

    def move_piece(self, name, source, destination, num_pieces):
        """Move desired number of player's pieces from source to destination on board"""

        # If it is the first turn of the game, set turn to name of player and set firstMove to True.
        if (self.turn == None):
            self.turn = name
            self.firstMove = True

        # If the first player's name is equal to the name of the player moving the piece, set the player's color to
        # the first player's color.  Otherwise, set color equal to second player's color.
        if (self._player1[0] == name):
            playerColor = self._player1[1]
        else:
            playerColor = self._player2[1]

        # If player who is playing this move is the same as the one who played the previous move,
        # and it is not the first move either, then it is not player's turn.
        if (self.turn == name and self.firstMove != True):
            return 'not your turn'

        # Otherwise check if the location the player entered is correct
        else:
            self.locationCheck(name, source, destination, num_pieces, playerColor)
            return 'successfully moved'


    def locationCheck(self, name, source, destination, num_pieces, playerColor):
        """Check if location the player entered is a valid location.  """

        row = destination[0]        # row of the destination
        column = destination[1]     # col of the destination
        row2 = source[0]            # row of the source
        column2 = source[1]         # col of the source

        # If the square you are moving from has no pieces
        if (len(self._board[row2][column2]) == 0):
            return 'invalid number of pieces'

        # If the piece at the top of the stack on that space does not match the player's color
        elif (self._board[row2][column2][-1] != playerColor):
            return 'invalid location'

        # If the space has less than the number of pieces the player wants to move, player is trying to move an
        # invalid number of pieces
        elif (len(self._board[row2][column2]) < num_pieces):
            return 'invalid number of pieces'

        # If the the row or column of the source square is more than 5, or the row or column of the destination
        # square is more than 5, then the player is moving the piece off the board or from a position not on the board.
        elif (source[0] > 5 or source[1] > 5 or destination[0] > 5 or destination[1] > 5):
            return 'invalid location'

        # If the the row or column of the source square is more than , or the row or column of the destination
        # square is more than , then the player is moving the piece off the board or from a position not on the board.
        elif (source[0] < 0 or source[1] < 0 or destination[0] < 0 or destination[1] < 0):
            return 'invalid location'

        # If the piece is trying to move diagonally
        elif (source[0] != destination[0] and source[1] != destination[1]):
            return 'invalid location'

        # If the row is the same, but the spaces that the player is trying to move horizontally along the board
        # is greater than the number of pieces the player is trying to move, the move is invalid
        elif (source[0] == destination[0] and (abs(source[1] - destination[1]) > num_pieces)):
            return 'invalid location'

        # If the column is the same, but the spaces that the player is trying to move vertically is greater than the
        # number of pieces the player is trying to move, the move is invalid
        elif (source[1] == destination[1] and (abs(source[0] - destination[0]) > num_pieces)):
            return 'invalid location'

        # If the space has no pieces
        elif len(self._board[source[0]][source[1]]) == 0:
            return 'invalid number of pieces '

        # Otherwise, move the piece to destination position.
        else:
            self.move_piece_finalized(name, source, destination, num_pieces, None)

    def move_piece_finalized(self, name, source, destination, num_pieces, player):
        """Move the piece to the destination after checking that it is a valid move."""

        row = destination[0]        # Row of the destination
        column = destination[1]     # Column of the destination
        row2 = source[0]            # Row of the source
        column2 = source[1]         # Column of the source

        # If player is moving a piece from a source to a destination, that is not from the player's reserves.
        if (source != "Reserves"):
            stack = self._board[row2][column2][-num_pieces:]                        # stack of pieces moving from the source
            self._board[row2][column2] = self._board[row2][column2][:-num_pieces]   # Source square contains the pieces left after stack of pieces is moved by player
            self._board[row][column].extend(stack)                                  # Add all the elements of the stack of pieces moved by player to the destination square
            self.firstMove = False

        # If player is playing a piece from the reserve.
        else:
            self._board[row][column].append(player[1])  # Add a single piece from the player's reserve to the space.
            self.firstMove = False

        # Set turn to the player that just played the move and update the player's number of reserve and captured pieces.
        self.turn = name
        self.updateScores(name, row, row2, column, column2)
        return 'successfully moved'




    def updateScores(self, name, row, row2, column, column2):
        """Update the player's reserve and captured number of pieces."""

        # If the space has more than than 5 pieces on it, remove the bottom piece.
        if len(self._board[row][column]) > 5:
            newStack = self._board[row][column][-5:]                                        # newStack gets the five topmost pieces
            removedStack = self._board[row][column][:len(self._board[row][column]) - 5]     # removedStack is the pieces that are removed from the bottom of the stack
            countGreen = removedStack.count('G')                                            # number of green pieces that are removed from the stack
            countRed = removedStack.count('R')                                              # number of red pieces that are removed form the stack

            # If the name of the player making the move is the same as player1's:
            if (self._player1[0] == name):
                color = self._player1[1]            # Set color equal to player1's color

                # If player1 is green and made the move, then add number of removed green piece to player1's reserve,
                # and add number of removed red piece to player1's captured number of pieces.
                if color == 'G':
                    self._player1_reserve = self._player1_reserve + countGreen
                    self._player1_captured = self._player1_captured + countRed

                # If player1 is red and made the move, then add removed red piece to player1's reserve,
                # and add number of removed green pieces to player1's captured number of pieces..
                if color == 'R':
                    self._player1_reserve = self._player1_reserve + countRed
                    self._player1_captured = self._player1_captured + countGreen

            # If the name of the player making the move is the same as player2's:
            if (self._player2[0] == name):
                color = self._player2[1]            # Set color equal to player2's color

                # If player2 is green and made the move, then add number of removed green piece to player2's reserve,
                # and add number of removed red piece to player2's captured number of pieces.
                if color == 'G':
                    self._player2_reserve = self._player2_reserve + countGreen
                    self._player2_captured = self._player2_captured + countRed

                # If player2 is red and made the move, then add removed red piece to player2's reserve,
                # and add number of removed green pieces to player2's captured number of pieces..
                if color == 'R':
                    self._player2_reserve = self._player2_reserve + countRed
                    self._player2_captured = self._player2_captured + countGreen

            # Set space to contain only the topmost five pieces of the stack after removing the bottom pieces.
            self._board[row][column] = self._board[row][column][-5:]


    def show_pieces(self, source):
        """Return the pieces on that square"""
        row = source[0]         # row of that square
        column = source[1]      # col of that square
        return self._board[row][column]

    def show_reserve(self, name):
        """Return how many pieces are in the player's reserve."""
        if (self._player1[0] == name):
            return self._player1_reserve
        elif (self._player2[0] == name):
            return self._player2_reserve
        else:
            return "INVALID NAME"

    def show_captured(self, name):
        """Return how many pieces are in that player's captured."""
        if (self._player1[0] == name):
            return self._player1_captured
        elif (self._player2[0] == name):
            return self._player2_captured
        else:
            return "INVALID NAME"

    def reserved_move(self, name, source):
        """Place a piece on the board from a player's reserve."""
        row = source[0]
        column = source[1]

        # If name of the player making a reserved move is equal to player1's name.
        if (self._player1[0] == name):

            # If player1 has no pieces in reserve.
            if (self._player1_reserve == 0):
                return 'no pieces in reserve'

            # Otherwise, place piece from player1's reserve onto board, and decrease reserve by 1.
            else:
                self.move_piece_finalized(name, "Reserves", source, 1, self._player1)
                self._player1_reserve = self._player1_reserve - 1

        # If name of the player making a reserved move is equal to player2's name.
        elif (self._player2[0] == name):

            # If player2 has no pieces in reserve.
            if (self._player2_reserve == 0):
                return 'no pieces in reserve'

            # Otherwise, place piece from player2's reserve onto board, and decrease reserve by 1.
            else:
                self.move_piece_finalized(name, "Reserves", source, 1, self._player2)
                self._player2_reserve = self._player2_reserve - 1

    def display_board(self):
        """Print out the board."""
        for row in self._board:
            print(str(row) + '\n')


"""
game = FocusGame(('PlayerA', 'R'), ('PlayerB','G'))


print("Initial Board:\n")
game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
game.display_board()
print('---------------------------')

game.move_piece('PlayerB', (1, 1), (2, 2), 1)
print("")
game.display_board()






game = FocusGame(('PlayerA', 'R'), ('PlayerB','G'))
game.move_piece('PlayerA',(0,0), (0,1), 1)  #Returns message "successfully moved"

game.show_pieces((0,1)) #Returns ['R','R']
game.show_captured('PlayerA') # Returns 0
game.reserved_move('PlayerA', (0,0)) # Returns message "No pieces in reserve"

game.show_reserve('PlayerA') # Returns 


print("Initial Board:\n")
game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
game.display_board()
print('---------------------------')

# Should not be allowed since (0, 0) is a red piece and PlayerB is green
# We must check color of piece before we move it (piece at last index is piece on top -check that one)
game.move_piece('PlayerA', (0, 0), (0, 1), 1)
print("")
game.display_board()
print('---------------------------')

game.move_piece('PlayerB', (0, 2), (0, 1), 1)
print("")
game.display_board()
print('---------------------------')

game.move_piece('PlayerA', (1, 2), (0, 2), 1)
print("")
game.display_board()
print('---------------------------')

game.move_piece('PlayerB', (1, 0), (0, 0), 1)
print("")
game.display_board()
print('---------------------------')

game.move_piece('PlayerA', (0, 2), (0, 1), 1)
print("")
game.display_board()
print('---------------------------')

game.move_piece('PlayerB', (0, 0), (0, 1), 1)
print("")
game.display_board()
print('---------------------------')

game.move_piece('PlayerA', (1, 3), (1, 2), 1)
print("")
game.display_board()
print('---------------------------')

# Show_reserve and show_captured methods do not display the number of reserve and captured pieces correctly.


# Correction:  Adds 1 to red captured, but I think that it should be adding to green capatured instead, because a green piece
# is adding on top of a stack with a bottom red piece

game.move_piece('PlayerB', (1, 1), (0, 1), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (1, 2), (1, 1), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (0, 3), (0, 2), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (1, 1), (0, 1), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (1, 4), (2, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.reserved_move('PlayerA', (0, 1))
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (2, 3), (2, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (2, 5), (2, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (3, 4), (2, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (3, 3), (2, 3), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (3, 5), (2, 5), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (3, 2), (3, 3), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (2, 5), (2, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (2, 3), (2, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (1, 5), (2, 5), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (3, 3), (3, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (2, 5), (2, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (3, 4), (4, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.reserved_move('PlayerB', (2, 4))
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (0, 1), (0, 2), 4)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (4, 2), (4, 3), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (4, 5), (4, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (5, 4), (4, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (5, 3), (5, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (4, 3), (4, 4), 2)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (5, 4), (4, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (5, 5), (5, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (5, 2), (5, 3), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (5, 4), (4, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (5, 3), (5, 4), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerB', (4, 2), (4, 3), 1)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

game.move_piece('PlayerA', (0, 2), (4, 2), 4)
print("")
game.display_board()
print("Player Green Reserves", game.show_reserve('PlayerB'))
print("Player Green Captured", game.show_captured('PlayerB'))
print("Player Red Reserves", game.show_reserve('PlayerA'))
print("Player Red Captured", game.show_captured('PlayerA'))
print('---------------------------')

"""
