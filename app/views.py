from flask import render_template, request, make_response
from app import app
import checkers
import json
from models import *
import string
import random
import sqlite3

user = {'nickname': 'Miguel'}  # fake user
moves_lst = ["0", "1", "2", "3", "4", "5", "6", "7"]
player_lst = ["R", "B"]
player_id_1 = "R"
player_id_2 = "B"
player_must_jump = False
player_must_move = None
game_id = ""
uppers = string.ascii_uppercase
lowers = string.ascii_lowercase
digits = string.digits
chars = uppers + lowers + digits


@app.route('/')
def start():
    global game_id
    print "start"

    game_id = "".join(random.choice(chars) for _ in range(6))
    print game_id
    x = checkers.Checkers(player_id_1, player_id_2)

    insert_game(game_id, x)

    print query_game(game_id)

    resp = render_template('start.html',
        title='Checkers',
        game_id=game_id,
        player_id_1=player_id_1,
        player_id_2=player_id_2)
    return resp

@app.route('/boardstate/<game_id>')
def board(game_id):
    
    x = query_board(str(game_id))
    while x is None:
        x = query_board(str(game_id))

    resp = json.dumps([x.board.return_board_3(), x.current_player.color])
    return resp


@app.route('/index/<game_id>/<player_id>')
def index(game_id, player_id):

    global player_must_move
    global player_must_jump

    row = request.args.get("row") or 0
    col = request.args.get("col") or 0
    to_row = request.args.get("to_row") or 0
    to_col = request.args.get("to_col") or 0

    row = int(row)
    col = int(col)
    to_row = int(to_row)
    to_col = int(to_col)

    x = query_board(str(game_id))
    while x is None:
        x = query_board(str(game_id))

    if player_must_move:
        row = player_must_move[0]
        col = player_must_move[1]

    if x.current_player.color != player_id:
        print "It's not your turn"
    elif not x.client_check_valid_piece(row, col):
        print "Invalid Piece Selected"
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

    update_game(game_id, x)

    board = x.board.return_board_3()

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
                           game_id=game_id,
                           player_id=player_id,
                           current_player=current_player))
    return resp

@app.route('/move/<row>/<col>/<to_row>/<to_col>')
def move_piece(row, col, to_row, to_col):
    row = int(row)
    col = int(col)
    to_row = int(to_row)
    to_col = int(to_col)
    x.board.make_move(row, col, to_row, to_col)
    return index()
