#!/usr/bin/env python

###############################################################################
#                                                                             #
#  apples.py                                                                  #
#                                                                             #
#    Apples-to-Apples classes                                                 #                                                         #
#                                                                             #
###############################################################################

import json
import random
import string

########################################################
# Globals                                              #
########################################################
CARDS_IN_HAND=5

with open('data/cards.json','r') as f:
    cards = json.load(f)

########################################################
# Classes                                              #
########################################################
class ApplesPlayer:
    def __init__(self, username, sid):
        super().__init__()
        self.username = username
        self.score = 0
        self.player_type = 'spectator'
        self.hand = [self.draw_card('red_cards') for _ in range(CARDS_IN_HAND)]
        self.played_card_idx = None
        self.id = sid
        self.selected_card = None

    def get_type(self):
    	return self.player_type

    def draw_card(self, card_type):
    	card = random.choice(cards[card_type])
    	return {
    		'item': card['item'],
    		'description': card['description']
    	}

    def serialize(self):
    	return {
    		'username': self.username,
    		'score': self.score,
    		'player_type': self.player_type,
    		'player_id': self.id,
    		'selected_card': self.selected_card
    	}

    def play_card(self, card):
    	for i, _card in enumerate(self.hand):
    		if card == _card['item']:
    			self.played_card_idx = i
    			self.selected_card = self.hand[i]

    def remove_and_draw_card(self):
    	self.hand.pop(index=self.played_card_idx)
    	self.hand.append(self.draw_card('red_card'))
    	self.played_card_idx = None
    	self.selected_card = None

    def get_hand(self):
    	return self.hand

    def change_type(self, new_type):
        self.player_type = new_type
        if new_type == 'winner':
            self.score += 1

class ApplesGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = {}
        self.status = 'lobby'
        self.selected_cards = None
        self.winning_card = None
        self.judge = None

    def get_player_ids(self):
    	return self.players.keys()

    def get

    def get_players(self):
    	return [self.players[pid] for pid in self.players.keys()]

    def get_state(self):
    	return {
    		'players': [player.serialize() for _, player in self.players.items()],
    		'status': self.status
    	}

    def get_selected_cards(self):
    	return [p.get_selected_card() for p in self.get_players()]

    def get_winning_card(self):
    	return self.winning_card

    def add_player(self, player_obj):
        self.players[player_obj.id] = player_obj
        print(f'added player: {player_obj}')

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
