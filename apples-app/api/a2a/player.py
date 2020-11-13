#!/usr/bin/env python

###############################################################################
#                                                                             #
#  player.py                                                                  #
#                                                                             #
#    Apples-to-Apples player class                                            #
#                                                                             #
###############################################################################

class ApplesPlayer:
	def __init__(self):
		pass

	def connect_to_server(self):
		raise NotImplementedError

	def draw_card(self):
		raise NotImplementedError

	def play_card(self):
		raise NotImplementedError

	def select_best_card(self):
		raise NotImplementedError

	def reset(self):
		raise NotImplementedError
		