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
CARDS_IN_HAND = 5
DEFAULT_CARD = {'item': 'default_card', 'description': 'default_desc'}

with open('data/cards.json','r') as f:
    cards = json.load(f)

########################################################
# Classes                                              #
########################################################
class ApplesPlayer:
    def __init__(self, username, sid):
        super().__init__()
        self.id = sid
        self.username = username
        self.score = 0
        self.player_type = 'spectator'
        self.hand = [self.draw_card('red_cards') for _ in range(CARDS_IN_HAND)]
        self.played_card_idx = None
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
    		'id': self.id,
    		'selected_card': self.selected_card
    	}

    def play_card(self, card_item):
    	for i, card in enumerate(self.hand):
    		if card_item == card['item']:
    			self.played_card_idx = i
    			self.selected_card = self.hand[i]

    def remove_and_draw_card(self):
    	self.hand.pop(self.played_card_idx)
    	self.hand.append(self.draw_card('red_cards'))
    	self.played_card_idx = None
    	self.selected_card = None

    def get_hand(self):
    	return self.hand

    def change_type(self, new_type):
        self.player_type = new_type


class ApplesGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = {}
        self.status = 'lobby'
        self.selected_cards = None
        self.selected_cards_and_players = None
        self.winner = None
        self.judge = None
        self.green_card = DEFAULT_CARD
        self.winner_timeout = 5

    def get_player_ids(self):
    	return self.players.keys()

    def get_player(self, player_id):
    	return self.players[player_id] if player_id in self.players else None

    def get_players(self):
    	return [self.players[pid] for pid in self.players.keys()]

    def get_players_by_type(self, p_type):
    	players = self.get_players()
    	players_by_type = []
    	for player in players:
    		if player.player_type == p_type:
    			players_by_type.append(player)
    	return players_by_type

    def set_players_to_type(self, type):
    	players = self.get_players()
    	for player in players:
    		player.change_type('active_player')

    def get_state(self):
    	return self.status

    def draw_green_card(self):
    	self.green_card = random.choice(cards['green_cards'])

    def get_selected_cards(self):
    	selected_cards, selected_cards_and_players = [], []
    	active_players = self.get_players_by_type('active_player')
    	print(active_players)

    	for player in active_players:
    		if player.selected_card:
    			selected_cards.append(player.selected_card)
    			selected_cards_and_players.append((player.id, player.selected_card))

    	if len(selected_cards) == len(active_players):
    		self.selected_cards_and_players = selected_cards_and_players
    		return selected_cards
    	else:
    		return None

    def remove_and_draw(self):
    	players = self.get_players_by_type('active_player')
    	for player in players:
    		player.remove_and_draw_card()

    def set_winner(self, card_item):
    	for cp in self.selected_cards_and_players:
    		(pid, selected_card) = cp
    		if selected_card['item'] == card_item:
    			self.winner = pid
    			winning_player = self.get_player(pid)
    			winning_player.score += 1

    def get_winner(self):
    	return self.winner

    def add_player(self, player_obj):
        self.players[player_obj.id] = player_obj
        print(f'added player: {player_obj}')

    def remove_player(self, player_id):
        self.players.pop(player_id, None)

    def make_someone_judge(self):
        current_judge = self.judge
        new_judge = random.choice(list(self.get_player_ids()))
        while current_judge == new_judge:
            new_judge = random.choice(list(self.get_player_ids()))
        self.judge = new_judge
        self.get_player(self.judge).change_type('judge')

    def debug_print(self):
    	judge = self.get_player(self.judge)
    	winner = self.get_player(self.winner)
    	dbg = '*'*20 + f' [{self.game_id}] ' + '*'*20
    	dbg += f'\nstatus: {self.status}'
    	dbg += f'\n# players: {len(self.get_players())}'
    	dbg += f'\nselected_card: {self.selected_cards}'
    	dbg += f'\nplayer types: {[p.player_type for p in self.get_players()]}'
    	dbg += f'\nsubmitted cards: {[p.selected_card for p in self.get_players()]}'
    	if judge:
    		dbg += f'\njudge: {judge.username}'
    	if winner:
    		dbg += f'\nwinner: {winner.username}'
    	dbg += '\n'+'*'*48
    	print(dbg)

    def game_logic(self):
    	self.debug_print()
    	if self.status == 'lobby':
            if len(self.get_players()) >= 3:
            	self.status = 'submission'
            	self.set_players_to_type('active_player')
            	self.make_someone_judge()
            	self.draw_green_card()
            	return

    	if self.status == 'submission':
        	selected_cards = self.get_selected_cards()
        	if selected_cards:
        		self.status = 'judging'
        		return

    	if self.status == 'judging':
        	winner = self.get_winner()
        	if winner:
        		self.status = 'winner_selected'
        		return

    	if self.status == 'winner_selected':
       		self.winner_timeout -= 1
       		if self.winner_timeout <= 0:
       			self.remove_and_draw()
       			self.set_players_to_type('active_player')
       			self.make_someone_judge()
       			self.draw_green_card()
       			self.winner = None
       			self.status = 'submission'
       			self.winner_time = 5
