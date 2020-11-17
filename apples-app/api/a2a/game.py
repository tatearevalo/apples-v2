#!/usr/bin/env python

###############################################################################
#                                                                             #
#  game.py                                                                    #
#                                                                             #
#    Apples-to-Apples game class                                              #
#                                                                             #
###############################################################################

from flask_socketio import SocketIO

class ApplesGame:
	def __init__(self, game_id):
		self.player_ct = 0
		self.id = game_id
		print(f'[Game] Game {self.id} created.')

	def create_server(self):
		raise NotImplementedError

	def start_game(self):
		raise NotImplementedError

	def play_hand(self):
		raise NotImplementedError

	def reset(self):
		raise NotImplementedError
