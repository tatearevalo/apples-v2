#!/usr/bin/env python3

###############################################################################
#                                                                             #
#  main.py                                                                    #
#                                                                             #
#    Scrapes Apples-to-Apples cards from the web                              #
#                                                                             #
###############################################################################

import json

import bs4

from scrape import AppleScraper

RED_CARDS_URL = 'http://www.com-www.com/applestoapples/applestoapples-red-with.html'
GREEN_CARDS_URL = 'http://www.com-www.com/applestoapples/applestoapples-green-with.html'
OUTPUT_FILENAME = 'cards.json'

if __name__=='__main__':

	apple_scraper = AppleScraper(
		red_url=RED_CARDS_URL,
		green_url=GREEN_CARDS_URL
	)

	output = {
		'red_cards': apple_scraper.scrape(apples='red'),
		'green_cards': apple_scraper.scrape(apples='green')
	}

	with open(OUTPUT_FILENAME, 'w') as f:
		json.dump(output, f)

	