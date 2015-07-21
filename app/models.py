from flask import Flask, g
import sqlite3

app = Flask(__name__)

DATABASE = "app/database.db"


def connect_to_database():
    return sqlite3.connect(DATABASE)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
        db.row_factory = sqlite3.Row
    return db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return(rv[0] if rv else None) if one else rv

def query_game(game_id):
    game = query_db('SELECT * FROM games WHERE game_id=?',[game_id])
    return game[0]

def query_current_player(game_id):
    game = query_game(game_id)
    return game['current_player'].encode("ascii")

def query_red_pieces(game_id):
    game = query_game(game_id)
    return game['red_pieces']

def query_blue_pieces(game_id):
    game = query_game(game_id)
    return game['blue_pieces']


def query_board(game_id):
    game = query_game(game_id)
    return game['board'].encode("ascii")


def insert_game(game_id, current_player,
                red_pieces, blue_pieces, board_state):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO games (game_id, current_player,\
                 red_pieces, blue_pieces, board_state) VALUES (?,?,?,?,?)",
                 (game_id, current_player, red_pieces, blue_pieces, board_state))
    db.commit()

def update_game(game_id, current_player,
                red_pieces, blue_pieces, board_state):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE games \
                    SET current_player=?,\
                        red_pieces=?,\
                        blue_pieces=?,\
                        board_state=?\
                    WHERE game_id=?",
        (current_player, red_pieces, blue_pieces, board_state, game_id))
    db.commit()