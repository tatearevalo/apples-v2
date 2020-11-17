#!/usr/bin/env python

###############################################################################
#                                                                             #
#  controller.py                                                              #
#                                                                             #
#    Apples-to-Apples game class                                              #
#                                                                             #
###############################################################################

from flask_socketio import SocketIO

from a2a.player import ApplesPlayer
from a2a.game import ApplesGame

class ApplesController:
	def __init__(self):
		self.id = 0
		self.games = {}
	
	def make_game(self):
		self.id += 1
		print(f'[Controller] Making game: id {self.id}')
		new_game = ApplesGame(self.id)
		self.games[self.id] = new_game
		return self.id

	def get_game(self, game_id):
		return self.games[game_id] if game_id in self.games else None

	def destroy_game(self):
		raise NotImplementedError
