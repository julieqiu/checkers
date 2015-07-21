from flask import Flask, g
import sqlite3
import pickle


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

def query_board(game_id):
    game = query_game(game_id)
    return pickle.loads(game['board_state'])


def insert_game(game_id, checkers_game):
    db = get_db()
    cursor = db.cursor()
    board = pickle.dumps(checkers_game)

    cursor.execute("INSERT INTO games (game_id, board_state)\
                    VALUES (?,?)",
                 (game_id, board))
    db.commit()

def update_game(game_id, checkers_game):
    db = get_db()
    cursor = db.cursor()
    board = pickle.dumps(checkers_game)
    cursor.execute("UPDATE games \
                    SET board_state=?\
                    WHERE game_id=?",
        (board, game_id))
    db.commit()
