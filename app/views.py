from flask import render_template, Markup
from app import app
import checkers

user = {'nickname': 'Miguel'}  # fake user
x = checkers.Checkers("1", "2")


@app.route('/')
@app.route('/index')
def index():
    board = Markup("<pre>" + x.board.return_board() + "</pre>")
    print board
    return render_template('index.html',
                           title='Checkers',
                           board=board,
                           user=user)


@app.route('/move/<row>/<col>/<to_row>/<to_col>')
def move_piece(row, col, to_row, to_col):
    row = int(row)
    col = int(col)
    to_row = int(to_row)
    to_col = int(to_col)
    return index()
