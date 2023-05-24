#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return "Index for Game/Review/User API"


@app.route( '/games' )
def games ( ) :
    games = Game.query.all()
    return games_response( games )


@app.route( '/games/' )
def redirect_to_games ( ) :
    return redirect( '/games' )


@app.route( '/games/<int:id>' )
def game_by_id ( id ) :
    game = Game.query.filter( Game.id == id ).first()
    if game :
        response = make_response( jsonify( game.to_dict() ), 200 )
        return response
    else :
        abort( 404 )

def game_to_dict ( game ) :
    return {
        'id': game.id,
        "title": game.title,
        'genre': game.genre,
        'platform': game.platform,
        'price': game.price
    }
    # return game.to_dict()

@app.route( '/games/title/<string:title>' )
def games_by_title ( title ) :
    games = Game.query.filter( Game.title.like( f'%{ title }%' ) ).order_by( Game.title ).all()
    if games :
        return games_response( games )
    else :
        response = make_response( 'Could not find any games by that title.', 404 )
        return response
    
    
@app.route( '/games/platform/<string:platform>' )
def games_by_platform ( platform ) :
    games = Game.query.filter( Game.platform.like( f'%{ platform }%' ) ).all() 
    if games :
        return games_response( games )
    else :
        response = make_response( 'Could not find any games with that platform.', 404 )
        return response
    

@app.route( '/games/genre/<string:genre>' )
def games_by_genre ( genre ) :
    games = Game.query.filter( Game.genre.like( f'%{ genre }%' ) ).all()
    if games :
        return games_response( games )
    else :
        response = make_response( 'Could not find games with that genre.', 404 )
        return response


def games_response ( games ) :
    games_to_dicts = [ game_to_dict( game ) for game in games ]
    response = make_response( jsonify( games_to_dicts ), 200 )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)