from flask import render_template, Markup, request, make_response
from app import app
import checkers

user = {'nickname': 'Miguel'}  # fake user
x = checkers.Checkers("1", "2")
moves_lst = ["0", "1", "2", "3", "4", "5", "6", "7"]
player_lst = ["R", "B"]
player_must_jump = False
player_must_move = None


@app.route('/')
@app.route('/index')
def index():

    global player_must_move
    global player_must_jump

    print "USER"
    user = request.cookies.get("user")
    print user

    try:
        row = request.args.get("row")
        col = request.args.get("col")
        to_row = request.args.get("to_row")
        to_col = request.args.get("to_col")

        row = int(row)
        col = int(col)
        to_row = int(to_row)
        to_col = int(to_col)

        if player_must_move:
            row = player_must_move[0]
            col = player_must_move[1]

        if not x.client_check_valid_piece(row, col):
            raise "Invalid Piece Selected"
        elif x.board.is_valid_move(row, col, to_row, to_col) and not \
        player_must_jump:
            x.board.make_move(row, col, to_row, to_col)
            x.switch_player()
        elif x.board.is_valid_jump(row, col, to_row, to_col):
            x.board.make_jump(row, col, to_row, to_col)
            row, col = to_row, to_col
            if not x.jump_available(row, col):
                x.switch_player()
                player_must_jump = False
                player_must_move = None
            else:
                player_must_jump = True
                player_must_move = [row, col]
        if x.check_game_over():
            print "Game Over"

    except Exception as e:
        print "exception raised"
        print e
        pass

    board = Markup("<pre>" + x.board.return_board() + "</pre>")
    current_player = x.current_player.color
    print board

    resp = make_response(
            render_template('index.html',
                           title='Checkers',
                           board=board,
                           user=user,
                           row=row,
                           col=col,
                           to_row=to_row,
                           to_col=to_col,
                           moves_lst=moves_lst,
                           current_player=current_player))
    return resp


@app.route('/set_user')
def set_user():
    user = request.args.get("user")
    resp = index()
    resp.set_cookie("user", user)
    return resp


@app.route('/move/<row>/<col>/<to_row>/<to_col>')
def move_piece(row, col, to_row, to_col):
    row = int(row)
    col = int(col)
    to_row = int(to_row)
    to_col = int(to_col)
    x.board.make_move(row, col, to_row, to_col)
    return index()
