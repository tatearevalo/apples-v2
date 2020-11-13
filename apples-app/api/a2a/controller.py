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
		self.games = []
	
	def make_game(self):
		print(f'[Controller] Making game: id {self.id}')
		new_game = ApplesGame(self.id)
		self.games.append((self.id, new_game))
		self.id += 1

	def destroy_game(self):
		raise NotImplementedError
