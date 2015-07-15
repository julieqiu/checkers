# Checkers Game

class Board:
    def __init__(self):
        self.row = 8
        self.column = 8
        self.red_pieces = 12
        self.black_pieces = 12
        # self.board = [[None for x in range(self.row)]
        #               for i in range(self.column)]

        # for row in range(3):
        #     for tile in range(8):
        #         if (row % 2) == (tile % 2):
        #             self.board[row][tile] = Piece("R")
        # for row in range(5, 8):
        #     for tile in range(8):
        #         if (row % 2) == (tile % 2):
        #             self.board[row][tile] = Piece("B")

        self.board = [[Piece("R"),None,Piece("R"),None,Piece("R"),None,Piece("R"), None],
                     [None,Piece("R"),None,None,None,Piece("R"),None,Piece("R")],
                     [Piece("R"),None,Piece("R"),None,Piece("R"),None,None,None],
                     [None,None,None,Piece("B"),None,None,None,Piece("R")],
                     [None,None,None,None,Piece("B"),None,Piece("B"),None],
                     [None,Piece("B"),None,Piece("B"),None,None,None,None],
                     [None,None,Piece("B"),None,Piece("B"),None,None,None],
                     [None,Piece("B"),None,Piece("B"),None,Piece("B"),None,Piece("B")]]

        # self.board = [[None,None,None,None,None,None,None,None],
        #              [None,None,None,None,None,None,None,None],
        #              [None,None,None,None,None,None,None,None],
        #              [None,None,None,None,None,None,None,None],
        #              [None,Piece("R"),None,None,None,None,None,None],
        #              [None,None,Piece("B"),None,None,None,None,None],
        #              [None,None,None,None,None,None,None,None],
        #              [None,None,None,None,None,None,None,None]]

    def lose_piece(self, color):
        if color == "R":
            self.red_pieces -= 1
        elif color == "B":
            self.black_pieces -= 1

    def draw_board(self):
        top_border = '|___|'
        for x in range(8):
            top_border = top_border + "|_" + str(x) + "_|"
        print top_border

        x = 0
        for row in self.board:
            array = "| " + str(x) + " |"
            for col in row:
                if col is None:
                    array += "|   |"
                else:
                    array += "| " + col.icon + " |"
            print array
            x += 1
        print self.red_pieces, self.black_pieces

    def return_board(self):
        top_border = '|___|'
        for x in range(8):
            top_border = top_border + "|_" + str(x) + "_|"
        x = 0
        for row in self.board:
            array = "|_" + str(x) + "_|"
            for col in row:
                if col is None:
                    array += "|___|"
                else:
                    array += "|_" + col.icon + "_|"
            top_border += "<br>" + array
            x += 1
        return top_border

    def return_board_2(self):
        array = ""

        for row in range(8):
            for col in range(8):
                tile = self.board[row][col]
                if tile is None:
                    if (row % 2 == col % 2):
                        array += "G"
                    else:
                        array += "W"
                else:
                    array += tile.icon
            array += "X"

        return array

    def return_board_3(self):
        array = []

        for row in range(8):
            items = []
            for col in range(8):
                tile = self.board[row][col]
                if tile is None:
                    if (row % 2 == col % 2):
                        items.append("G")
                    else:
                        items.append("W")
                else:
                    items.append(tile.icon)
            array += [items]

        return array

    def make_jump(self, row, col, to_row, to_col):
        jump_row = abs((row + to_row) / 2)
        jump_col = abs((col + to_col) / 2)
        self.board[to_row][to_col] = self.get_piece(row, col)
        self.lose_piece(self.get_piece(jump_row, jump_col).color)
        if self.is_king_row(row, col, to_row, to_col) is True:
            self.get_piece(row, col).make_king()
        self.board[row][col] = None
        self.board[jump_row][jump_col] = None

    def make_move(self, row, col, to_row, to_col):
        self.board[to_row][to_col] = self.get_piece(row, col)
        if self.is_king_row(row, col, to_row, to_col) is True:
            self.get_piece(row, col).make_king()
        self.board[row][col] = None

    def is_king_row(self, row, col, to_row, to_col):
        piece = self.get_piece(row, col)
        piece_color = piece.color
        if (to_row == 0 and piece_color == "B"):
            return True
        if (to_row == 7 and piece_color == "R"):
            return True
        else:
            return False

    def contains_piece(self, row, col):
        return self.board[row][col] is not None

    def is_valid_jump(self, row, col, to_row, to_col):
        if (to_row > 7) or (to_row < 0) or (to_col > 7) or (to_col < 0):
            print "Move goes beyond the board"
            return False

        if self.contains_piece(to_row, to_col):
            print "There's a piece at ", to_row, to_col
            return False

        if not ((to_col == col + 2) or (to_col == col - 2)):
            print "Invalid Jump! Can't move to that position"
            return False

        # Checks if piece is moving in the right direction:
        piece = self.get_piece(row, col)
        piece_color = piece.color
        piece_type = piece.type

        if piece_color == "R" and piece_type == "regular":
            if (to_row - row) != 2:
                print row
                print col
                print to_row
                print to_col
                print "A regular red piece can't move there!"
                return False
        if piece_color == "B" and piece_type == "regular":
            if (row - to_row) != 2:
                print "A regular black piece can't move there!"
                return False
        if piece_type == "king":
            if abs(row - to_row) != 2:
                print "A king can't move there!"
                return False

        # Checks if there is a piece to jump
        jump_row = (row + to_row) / 2
        jump_col = (col + to_col) / 2
        if self.get_piece(jump_row, jump_col) is None:
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
        self.icon = color

    def make_king(self):
        self.type = "king"
        self.icon = self.color.lower()


class Player:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.pieces = 12


class Checkers:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = Player("R", player1)
        self.player2 = Player("B", player2)
        self.player1.next_player = self.player2
        self.player2.next_player = self.player1
        self.current_player = self.player1

    def switch_player(self):
        self.current_player = self.current_player.next_player

    def check_game_over(self):
        if self.board.red_pieces == 0 or self.board.black_pieces == 0:
            return True
        return False

    def select_piece(self):

        valid_piece = False
        while not valid_piece:
            row = ' '
            col = ' '
            print self.current_player.name + \
                ", which piece would you like to move?"
            while not (row.isdigit() and 0 <= int(row) < 8):
                row = raw_input("Row: ")
            while not (col.isdigit() and 0 <= int(row) < 8):
                col = raw_input("Column: ")

            row = int(row)
            col = int(col)
            print row
            print col

            if not self.board.contains_piece(row, col):
                print "There's no piece there!"
                continue

            if self.board.get_piece(row, col).color != \
               self.current_player.color:
                print "That's not your piece!"
                continue
            valid_piece = True

        return row, col

    def client_check_valid_piece(self, row, col):
        if not self.board.contains_piece(row, col):
            print "There's no piece there!"
            return False

        if self.board.get_piece(row, col).color != \
           self.current_player.color:
            print "That's not your piece!"
            return False

        return True

    def select_move(self):
        to_row = ' '
        to_col = ' '

        print self.current_player.name + \
            ", where would you like to move it to?"
        while not ((to_row).isdigit() and 0 <= int(to_row) < 8):
            to_row = raw_input("Row: ")
        while not ((to_col).isdigit() and 0 <= int(to_col) < 8):
            to_col = raw_input("Column: ")

        return int(to_row), int(to_col)

    def jump_available(self, row, col):
        if self.board.is_valid_jump(row, col, row - 2, col - 2):
            return True
        if self.board.is_valid_jump(row, col, row - 2, col + 2):
            return True
        if self.board.is_valid_jump(row, col, row + 2, col - 2):
            return True
        if self.board.is_valid_jump(row, col, row + 2, col + 2):
            return True
        else:
            return False

    def start_game(self):
        self.board.draw_board()
        playing_game = True
        while playing_game:
            is_valid_move = False
            while not is_valid_move:
                row, col = self.select_piece()
                to_row, to_col = self.select_move()

                if self.board.is_valid_move(row, col, to_row, to_col):
                    self.board.make_move(row, col, to_row, to_col)
                    is_valid_move = True
                elif self.board.is_valid_jump(row, col, to_row, to_col):
                    self.board.make_jump(row, col, to_row, to_col)
                    self.board.draw_board()
                    print "made jump from ", row, col, "to ", to_row, to_col
                    row, col = to_row, to_col
                    while self.jump_available(row, col):
                        print "jump available"
                        to_row, to_col = self.select_move()
                        print "selected new move"
                        if self.board.is_valid_jump(row, col, to_row, to_col):
                            self.board.make_jump(row, col, to_row, to_col)
                            row, col = to_row, to_col
                    is_valid_move = True
                self.board.draw_board()
                playing_game = not(self.check_game_over())
            self.switch_player()
            self.board.draw_board()

if __name__ == '__main__':
    x = Checkers(raw_input("Player 1: "), raw_input("Player 2: "))
    x.start_game()
