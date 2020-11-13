#!/usr/bin/env python3

###############################################################################
#                                                                             #
#  main.py                                                                    #
#                                                                             #
#    Scrapes Apples-to-Apples cards from the web and dumps to csv             #
#                                                                             #
###############################################################################

import csv
import json

import bs4

from scrape import AppleScraper

RED_CARDS_URL = 'http://www.com-www.com/applestoapples/applestoapples-red-with.html'
GREEN_CARDS_URL = 'http://www.com-www.com/applestoapples/applestoapples-green-with.html'

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

def write_to_csv(filename, cards):
	w = csv.writer(open(filename))
	for idx, card in enumerate(cards):
		row = [str(idx)] + [str(card[f]) for f in FIELDS[1:]]
		cleaned_row = [field.replace(',','') for field in row]
		w.writerow(cleaned_row)

if __name__=='__main__':

	apple_scraper = AppleScraper(
		red_url=RED_CARDS_URL,
		green_url=GREEN_CARDS_URL
	)

	# scrape into json/dict
	red_cards = apple_scraper.scrape(apples='red'),
	green_cards = apple_scraper.scrape(apples='green')

	# dump output
	write_to_csv(RED_CSV, red_cards)
	write_to_csv(GREEN_CSV, green_cards)

	print('Complete')
	