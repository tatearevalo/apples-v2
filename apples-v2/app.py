#!/usr/bin/env python

###############################################################################
#                                                                             #
#  application.py                                                             #
#                                                                             #
#    Apples-to-Apples web application                                         #
#                                                                             #
###############################################################################

import os
import random
import string
import time

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, join_room, leave_room, send, emit

CARDS_IN_HAND=5
MAX_REQUEST_LEN=25

app = Flask(__name__)
socketio = SocketIO(app)
games = []
scores = {}

########################################################
# Template Rendering                                   #
########################################################

@app.route("/", methods=['GET', 'POST'])
def display_home():
    return render_template("index.html")

@app.route("/rules")
def display_rules():
    return render_template('rules.html')

@app.route("/game/<string:game_id>")
def display_game(game_id):
    cards, players = [], []
    
    for i in range(CARDS_IN_HAND):
        cards.append(draw_card())

    return render_template(
        'game.html',
        game_id=game_id,
        cards=cards,
        players=scores[game_id]
    )

@app.route("/judge")
def display_judge(msg):
    return render_template('judge.html')

########################################################
# Utility Methodss                                     #
########################################################
def draw_card():
    # TODO query DB
    return {'item': 'myitem', 'desc': 'mydesc'}

def create_game():
    letters = string.ascii_letters
    new_game = ''.join(random.choice(letters) for i in range(4))
    games.append(new_game)
    scores[new_game] = []
    return new_game

########################################################
# Socket Communication                                 #
########################################################
@socketio.on('connect')
def connection_handler():
    print('[server] connected with client')

@socketio.on('create_game_request')
def create_game_handler():
    game = create_game()
    print(game)
    emit('game_created', {'game':game})

@socketio.on('join_game')
def join_game(msg):
    print('[server] joining game')
    if msg['game_id'] in games:
        join_room(msg['game_id'])

        scores[msg['game_id']].append({
            'username':msg['username'],
            'score':0
        })

        response = {
            'joined_game': True,
            'game_id': msg['game_id'],
            'username': msg['username']
        }
        send(response, room=msg['game_id'])

@socketio.on('leave_game')
def leave_game(msg):
    leave_room(msg['game_id'])
    response = {
        'join_game': True,
        'game_id': msg['game_id']
    }
    if msg['username'] in players:
        players.pop(msg['username'], None)

    send(response, room=msg['game_id'])

if __name__ == "__main__":
    socketio.run(app, debug=True)
