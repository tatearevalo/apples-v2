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

CARDS_IN_HAND=5
MAX_REQUEST_LEN=25
UPDATE_TIME = 1 # seconds

app = Flask(__name__)
socketio = SocketIO(app)
room_list = {}

with open('data/cards.json','r') as f:
    cards = json.load(f)

class Player:
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        self.player_type = 'default_player'
        self.score = 0
        self.hand = [self.draw_card('red_cards') for _ in range(CARDS_IN_HAND)]

    def draw_card(self, card_type):
        return random.choice(cards[card_type])

    def change_type(self, new_type):
        self.player_type = new_type
        if new_type == 'winner':
            self.score += 1


class ApplesGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = {}
        self.status = 'lobby'
        self.judge = None

    def add_player(self, player_obj):
        self.players[player_obj.id] = player_obj

    def remove_player(self, player_id):
        self.players.pop(player_id, None)

    def make_judge(self):
        current_judge = self.judge
        new_judge = random.choice(list(self.players))
        while current_judge == new_judge:
            new_judge = random.choice(list(self.players))
        self.judge = new_judge

    def start_game(self):
        if len(self.players) < 3 and self.states == 'lobby':
            return
        self.status = 'started'

    def game_logic(self):
        if self.status == 'lobby':
            return
        if self.status == 'started':
            pass

    def get_updated_state(self):
        return {
            'update_game': True,
            'players': self.players,
            'status': self.status
        }


########################################################
# Template Rendering                                   #
########################################################

@app.route("/", methods=['GET', 'POST'])
def display_home():
    return render_template("combined.html")

########################################################
# Update Loop                                           #
########################################################
def update_loop():
    while app is None:
        time.sleep(UPDATE_TIME)

    while True:
        time.sleep(UPDATE_TIME)
        for game_id in list(room_list):
            game = room_list[game_id]
            print(f'[update loop] game_id: {game_id}')
            game.game_logic()
            update = game.get_updated_state()
            socketio.send(update, room=game_id)
            # emit(room_list[game])   


########################################################
# Utility Methods                                      #
########################################################
def create_game():
    letters = string.ascii_letters
    new_game_id = ''.join(random.choice(letters) for i in range(4))
    new_game = ApplesGame(new_game_id)
    room_list[new_game_id] = new_game
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
    # emit('game_created', {'game':game})

@socketio.on('join_game')
def join_game(msg):
    game_id = msg['game_id']
    print('[server] joining game')
    if game_id in room_list.keys():
        join_room(game_id)

        new_player = Player(username=msg['username'])
        room_list[game_id].add_player(new_player)

        # debugging
        response = {
            'joined_game': True,
            'game_id': game_id,
            'username': msg['username']
        }
        send(response, room=game_id)

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
    game_thread = threading.Thread(target=update_loop)
    game_thread.start()
    socketio.run(app, debug=True)
