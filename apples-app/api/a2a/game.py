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
	def __init__(self):
		pass

	def create_server(self):
		raise NotImplementedError

	def start_game(self):
		raise NotImplementedError

	def play_hand(self):
		raise NotImplementedError

	def reset(self):
		raise NotImplementedError
		