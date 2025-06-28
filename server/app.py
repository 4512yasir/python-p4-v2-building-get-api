# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here

# server/app.py
@app.route('/games')
def get_games():
    games = [game.to_dict() for game in Game.query.all()]
    response = make_response(games, 200)
    return response

@app.route('/games/<int:id>')
def get_game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    if game:
        response = make_response(game.to_dict(), 200)
    else:
        response = make_response({'error': 'Game not found'}, 404)
    return response


@app.route('/games/users/<int:id>')
def get_game_users(id):
    game = Game.query.filter(Game.id == id).first()
    if game:
        users = [user.to_dict(rules=('-reviews',)) for user in game.users]
        response = make_response(users, 200)
    else:
        response = make_response({'error': 'Game not found'}, 404)
    return response



if __name__ == '__main__':
    app.run(port=5556, debug=True)

