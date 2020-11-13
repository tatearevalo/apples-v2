#!/usr/bin/env python3

###############################################################################
#                                                                             #
#  json_to_csv.py                                                             #
#                                                                             #
#    Create csv files from json                                               #
#                                                                             #
###############################################################################

import csv
import json

FN='cards.json'
RED_CSV='red_cards.csv'
GREEN_CSV='green_cards.csv'

FIELDS = [
	'id',
	'item',
	'description',
	'party_set',
	'basic_set',
	'junior_set',
	'expansion_set_1',
	'expansion_set_2',
	'expansion_set_3',
	'expansion_set_4',
	'party_expansion_set'
]

if __name__=='__main__':

	with open(FN,'r') as f:
		cards = json.load(f)

	red_cards = cards['red_cards']
	green_cards = cards['green_cards']

	rf = csv.writer(open(RED_CSV,'w'))
	gf = csv.writer(open(GREEN_CSV,'w'))

	for idx, card in enumerate(red_cards):
		row = [str(idx)] + [str(card[f]) for f in FIELDS[1:]]
		cleaned_row = [field.replace(',','') for field in row]
		rf.writerow(cleaned_row)

	for idx, card in enumerate(green_cards):
		row = [str(idx)] + [str(card[f]) for f in FIELDS[1:]]
		cleaned_row = [field.replace(',','') for field in row]
		gf.writerow(cleaned_row)

	print('Complete')