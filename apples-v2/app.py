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
UPDATE_TIME = 3
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
            game = room_list[game_id]
            game.game_logic()

            players = []
            # messages to each individual player
            for player_id in game.get_player_ids():
                player = game.players[player_id]
                players.append(player.serialize())
                hand = player.get_hand() # if player.get_type() != 'spectator' else []
                player_update = {'hand': hand}
                socketio.emit('update_hand', player_update, room=player_id)

            # message to entire room
            game_update = {
                'state': game.get_state(),
                'selected_cards': game.get_selected_cards(),
                'players': players,
                'green_card': [game.green_card]
            }
            if game.get_winner() is not None:
                game_update['winner_id'] = game.get_winner()

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

@socketio.on('red_card_submission')
def red_card_submission_handler(msg):
    print(f"received red card: {msg['card_item']}")
    player_id = request.sid
    game_id = msg['game_id']
    card_item = msg['card_item']
    game = room_list[game_id]
    player = room_list[game_id].get_player(player_id)
    if player_id != game.judge:
        player.play_card(card_item)
    else:
        game.set_winner(card_item)
    print(f'received red card submission: {card_item}')

@socketio.on('join_game')
def join_game(msg):
    sid = request.sid
    game_id = msg['game_id']
    print('[server] joining game')
    if game_id in room_list.keys():
        join_room(game_id)

        new_player = ApplesPlayer(username=msg['username'], sid=sid)
        room_list[game_id].add_player(new_player)

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
