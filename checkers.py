# Checkers Game

class Board:
    def __init__(self):
        self.row = 8
        self.column = 8
        self.board = [[None for x in range(self.row)] for i in range(self.column)]

        for row in range(3):
            for tile in range(8):
                if (row % 2) == (tile % 2):
                    self.board[row][tile] = Piece("R")
        for row in range(5, 8):
            for tile in range(8):
                if (row % 2) == (tile % 2):
                    self.board[row][tile] = Piece("B")


    def draw_board(self):
        top_border = [' ']
        for x in range(8):
            top_border.append(str(x))
        print top_border

        x = 0
        for row in self.board:
            array = [str(x)]
            for col in row:
                if col == None:
                    array += " "
                else:
                    array += col.color
            print array
            x += 1

    def move_piece(self, row, col, to_row, to_col):
        if self.is_valid_jump(row, col, to_row, to_col):
            jump_row = abs((row+to_row)/2)
            jump_col = abs((col+to_col)/2)
            self.board[to_row][to_col] = self.get_piece(row, col)
            self.board[row][col] = None
            self.board[jump_row][jump_col] = None
            return True
        if self.is_valid_move(row, col, to_row, to_col):
            self.board[to_row][to_col] = self.get_piece(row, col)
            self.board[row][col] = None
            return True
        return False

    def contains_piece(self, row, col):
        if self.board[row][col] == None:
            return False
        else:
            return True

    def is_valid_jump(self, row, col, to_row, to_col):
        if self.contains_piece(to_row, to_col):
            print "There's a piece at %d, %d", to_row, to_col
            return False
        if (to_row > 7) or (to_row < 0) or (to_col > 7) or (to_col < 0):
            print "Move goes beyond the board"
            return False
        if not ((to_col == col + 2) or (to_col == col -2)):
            print "Invalid Jump! Can't move to that position"
            return False

        jump_row = abs((row + to_row) / 2)
        jump_col = abs((col + to_col) / 2)
        if self.get_piece(jump_row, jump_col) == None:
            print jump_row
            print jump_col
            print self.get_piece(jump_row, jump_col)
            print "Invalid jump! There is no piece to jump"
            return False

        opp_color = self.get_piece(jump_row, jump_col).color
        curr_color = self.get_piece(row, col).color

        if opp_color == curr_color:
            print "Invalid Jump! Cannot jump your own piece"
            return False

        return True



        # if the it jumps over an opposing player's piece
        # if the piece that it is moving to does not contain a piece

    def is_valid_move(self, row, col, to_row, to_col):
        piece = self.get_piece(row, col)

        if self.contains_piece(to_row, to_col):
            print "There's a piece at %d, %d", to_row, to_col
            return False
        if (to_row > 7) or (to_row < 0) or (to_col > 7) or (to_col < 0):
            print "Move goes beyond the board"
            return False
        if not ((to_col == col + 1) or (to_col == col - 1)):
            print "Cannot move to the position"
            return False
        if piece.type == "regular":
            if (piece.color == "R"):
                if to_row != row + 1:
                    print "Red piece cannot move to that position"
                    return False
            if (piece.color == "B"):
                if to_row != row - 1:
                    print "Blue piece cannot move to that position"
                    return False
        if piece.type == "king":
            if not (to_row == row - 1 or to_row == row + 1):
                print "Invalid King Move"
                return False
        return True

    def get_piece(self, row, col):
        return self.board[row][col]


class Piece:
    def __init__(self, color):
        self.color = color
        self.type = "regular"

    def make_king(self):
        self.type = "king"

class Player:
    def __init__(self, color, name):
        self.color = color
        self.name = name

class Checkers:
    def __init__(self):
        self.board = Board()
        self.player1 = Player("R", raw_input("Player 1: "))
        self.player2 = Player("B", raw_input("Player 2: "))
        self.current_player = self.player1
        self.board.draw_board()

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def start_game(self):
        playingGame = True
        while playingGame == True:
            validMove = False
            while validMove == False:

                row = ' '
                col = ' '

                print self.current_player.name + ", which piece would you like to move?"
                while not ((row).isdigit() and 0 <= int(row) < 8):
                    row = raw_input("Row: ")
                while not ((col).isdigit() and 0 <= int(row) < 8):
                    col = raw_input("Column: ")

                row = int(row)
                col = int(col)

                if not self.board.contains_piece(row,col):
                    print "There's no piece there!"
                    continue

                if self.board.get_piece(row, col).color != self.current_player.color:
                    print "That's not your piece!"
                    continue

                to_row = ' '
                to_col = ' '

                print self.current_player.name + ", where would you like to move it to?"
                while not ((to_row).isdigit() and 0 <= int(row) < 8):
                    to_row = raw_input("Row: ")
                while not ((to_col).isdigit() and 0 <= int(row) < 8):
                    to_col = raw_input("Column: ")

                to_row = int(to_row)
                to_col = int(to_col)


                validMove = self.board.move_piece(int(row), int(col), int(to_row), int(to_col))
            self.switch_player()
            self.board.draw_board()



x = Checkers()
x.start_game()