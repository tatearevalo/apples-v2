#!/usr/bin/env python

###############################################################################
#                                                                             #
#  application.py                                                             #
#                                                                             #
#    Apples-to-Apples web application                                         #
#                                                                             #
###############################################################################

import json
import os
import random
import string
import threading
import time

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from apples import ApplesGame, ApplesPlayer

########################################################
# Globals                                              #
########################################################
UPDATE_TIME = 3  # seconds
MAX_REQUEST_LEN=25

app = Flask(__name__)
socketio = SocketIO(app)
room_list = {}

########################################################
# Template Rendering                                   #
########################################################

@app.route("/", methods=['GET', 'POST'])
def display_home():
    return render_template("apples.html")

########################################################
# Update Loop                                          #
########################################################
def update_loop():
    while app is None:
        time.sleep(UPDATE_TIME)

    while True:
        time.sleep(UPDATE_TIME)
        for game_id in list(room_list):
            print(f'[update loop] game_id: {game_id}')
            game = room_list[game_id]
            players = []

            # messages to each individual player
            for player_id in game.get_player_ids():
                player = game.players[player_id]
                players.append(player.serialize())
                hand = player.get_hand() if player.get_type() != 'spectator' else []
                player_update = {'player_hand': hand}
                socketio.emit('update_hand', player_update, room=player_id)

            # message to entire room
            game_update = {
                'state': game.get_state(),
                'players': players
            }
            socketio.emit('update_game', game_update, room=game_id)

########################################################
# Utility Methods                                      #
########################################################
def create_game():
    letters = string.ascii_letters
    new_game_id = ''.join(random.choice(letters) for i in range(4))
    new_game = ApplesGame(new_game_id)
    room_list[new_game_id] = new_game
    return new_game_id

########################################################
# Socket Communication                                 #
########################################################
@socketio.on('connect')
def connection_handler():
    sid = request.sid
    join_room(sid)
    print(f'socket id: {sid}')
    emit('create_id', {'your_id':sid}, room=sid)

@socketio.on('disconnect')
def connection_disconnected():
    sid = request.sid
    leave_room(sid)
    print('Client disconnected')

@socketio.on('create_game_request')
def create_game_handler():
    game = create_game()
    emit('game_created', {'game':game})

# @socketio.on('start_game')
# def game_start(msg):
#     room = msg.room

@socketio.on('join_game')
def join_game(msg):
    sid = request.sid
    game_id = msg['game_id']
    print('[server] joining game')
    if game_id in room_list.keys():
        join_room(game_id)

        new_player = ApplesPlayer(username=msg['username'], sid=sid)
        room_list[game_id].add_player(new_player)

        print(get_players_attrs(game_id))

        response = {
            'game_id': game_id,
            'player_init': get_players_attrs(game_id),
            'new_player': {
                'username': new_player.username,
                'id': new_player.id,
                'player_type': new_player.player_type
            }
        }
        emit('joined_game', response, room=game_id)

def get_players_attrs(game_id):
    players = []
    for player in room_list[game_id].get_players():
        players.append({
            'username': player.username,
            'id': player.id,
            'player_type': player.player_type
        })
    return players

@socketio.on('leave_game')
def leave_game():
    pass
    """
    leave_room(msg['game_id'])
    response = {
        'leave_game': True,
        'game_id': msg['game_id']
    }
    if msg['username'] in players:
        players.pop(msg['username'], None)

    send(response, room=msg['game_id'])
    """

if __name__ == "__main__":
    game_thread = threading.Thread(target=update_loop)
    game_thread.start()
    socketio.run(app, debug=True)
