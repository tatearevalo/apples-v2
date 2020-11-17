#!/usr/bin/env python

###############################################################################
#                                                                             #
#  player.py                                                                  #
#                                                                             #
#    Apples-to-Apples player class                                            #
#                                                                             #
###############################################################################

import random
import string
import time

from flask import Flask
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from a2a.controller import ApplesController
from a2a.game import ApplesGame
from a2a.player import ApplesPlayer

MAX_REQUEST_LEN=25

app = Flask(__name__)
socketio = SocketIO(app)
a2a_controller = ApplesController()
games = []

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

def create_game():
	letters = string.ascii_letters
	new_game = ''.join(random.choice(letters) for i in range(5))
	games.append(new_game)
	print(f'game created: {new_game}')
	return new_game

@socketio.on('connect')
def connection_handler():
	print('[server] connect')

@socketio.on('message')
def message_handler(message):
	print(f'[server] received message: {message}')
	msg_type = message['type']
	msg_data = message['data']
	response = {}

	if len(msg_data) > MAX_REQUEST_LEN:
		print('Bad request. Exceeded max length')
		return None

	if msg_type == 'create_game_request':
		response['new_game'] = create_game()
		send(response)
	
	if msg_type == 'join_game':
		if msg_data in games:
			print('Game found!')
			response['join_game'] = True
			response['game_id'] = data
			send(response)
		else:
			print('Game not found :(')
			response['game_not_found'] = f'Game {msg_data} does not exist'

"""
@socketio.on('join')
def on_join(data):
	print('joining')
	username = data['username']
	game = data['game']
	join_room(game)

@socketio.on('leave')
def on_leave(data):
	username = data['username']
	game = data['game']
	leave_room(game)
"""

if __name__=='__main__':
	socketio.run(app, debug=True)
