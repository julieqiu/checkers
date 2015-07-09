from flask import render_template, Markup, redirect
from app import app
import checkers

user = {'nickname': 'Miguel'}  # fake user
x = checkers.Checkers("1","2")

@app.route('/')
@app.route('/index')
def index():
    board = Markup("<pre>" + x.board.return_board() + "</pre>")
    print board
    return render_template('index.html',
                           title='Home',
                           board=board,
                           user=user)

@app.route('/move/<row>/<col>/<to_row>/<to_col>')
def move_piece(row, col, to_row, to_col):
    x.board.make_move(row, col, to_row, to_col)
    # board = Markup("<pre>" + x.board.return_board() + "</pre>")
    # print board
    # return render_template('index.html',
    #                        title='Home',
    #                        board=board,
    #                        user=user)