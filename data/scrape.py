#!/usr/bin/env/python3

###############################################################################
#                                                                             #
#  scrape.py                                                                  #
#                                                                             #
#    Contains a class for scraping Apples-to-Apples cards                     #
#                                                                             #
###############################################################################

import ast
import re
import urllib.request

import bs4

class AppleScraper:
	"""A simple Apples-to-Apples web scraping class.

	:param red_url: url to the Apples-to-Apples webpage of red cards
	:type red_url: str, required
	:param green_url: url to the Apples-to-Apples webpage of green cards
	:type green_url: str, required
	"""
	def __init__(self, red_url, green_url):
		self.red_soup = AppleScraper.url_to_soup(red_url)
		self.green_soup = AppleScraper.url_to_soup(green_url)
		self.set_map = {
			'Basic Set': 'basic_set',
			'Party Set': 'party_set',
			'Expansion Set 1': 'expansion_set_1',
			'Expansion Set 2': 'expansion_set_2',
			'Expansion Set 3': 'expansion_set_3',
			'Expansion Set 4': 'expansion_set_4',
			'Party Expansion': 'party_expansion_set'
		}


	def scrape(self, apples='red'):
		"""A method which scrapes Apples-to-Apples cards.

		:param apples: Defines whether to use 'Red Cards' or 'Green Cards'
		:type apples: (str, valid options: ['red','green'])
		:return: A list of cards
		:rtype: Python list
		"""
		soup = self.red_soup if apples == 'red' else self.green_soup
		cards = []

		for li in soup.find_all('ul')[0]:
			card = self.create_card(li)
			if AppleScraper.is_card_valid(card):
				cards.append(card)

		return cards


	def create_card(self, li):
		"""Creates a card

		:param li: html list element containing card information
		:type li: html element
		:return: a card containing the item name, description, and which
		         Apples-to-Apples sets it belongs to
		:rtype: python dict
		"""
		card = AppleScraper.default_card()

		if len(li) < 2:
			return card

		for item in li:
			if isinstance(item, bs4.element.Tag):
				if item.name == 'b':
					card['item'] = item.contents[-1]
				if item.name == 'i':
					card['description'] += item.contents[-1]
				if item.name == 'u':
					card = self.add_sets(card, item)
			elif item[-1] != '\n':
				card['description'] = AppleScraper.clean_description(str(item))

		return card


	def add_sets(self, card, item):
		"""Updates the card with the Apples-to-Apples' sets that the card
		belongs to. For example 'Party Set', 'Basic Set', 'Expansion Set 1', etc.
		
		:param card: an Apples-to-Apples card
		:type card: python dict
		:param item: element specifying the sets a card belongs to
		:type item: <u> html element
		:return: an Apples-to-Apples card
		:rtype: python dict
		"""

		# format the list for literal evaluation
		_item = item.contents[-1]
		_item = re.sub('\[','["', _item)
		_item = re.sub('\]','"]', _item)
		_item = re.sub(', ','","', _item)

		try:
			gamesets = ast.literal_eval(_item)
		except SyntaxError:
			return None

		for gameset in gamesets:
		 	if gameset in self.set_map:
		 		card[self.set_map[gameset]] = True
		 	elif 'Junior' in gameset:
		 		card['junior_set'] = True
		 	elif 'Basic Set' in gameset:
		 		card['basic_set'] = True

		return card


	@staticmethod
	def is_card_valid(card):
		"""Determines if a card is valid or not.
		
		:param card: an Apples-to-Apples card
		:type card: python dict
		:return: true if valid else false
		:rtype: boolean
		"""
		if not card or not card['item'] or not card['description']:
			return False

		for key in card:
			if key == 'item' or key == 'description':
				pass
			if card[key] == True:
				return True

		return False


	@staticmethod
	def default_card():
		"""@staticmethod which creates a default Apples-to-Apples card

		:return: an Apples-to-Apples card
		:rtype: python dict
		"""
		return {
			'item': None,
			'description': None,
			'party_set': False,
			'basic_set': False,
			'junior_set': False,
			'expansion_set_1': False,
			'expansion_set_2': False,
			'expansion_set_3': False,
			'expansion_set_4': False,
			'party_expansion_set': False
		}


	@staticmethod
	def clean_description(description):
		"""@staticmethod which cleans an Apples-to-Apples description

		:param description: an Apples-to-Apples description
		:type description: str
		:return: cleaned Apples-to-Apples description
		:rtype: str
		"""
		return re.sub(' - ', '', description)


	@staticmethod
	def url_to_soup(url):
		"""@static method which converts a url to a BeautifulSoup object

		:param url: the desired url
		:type url: str
		:return: webpage
		:rtype: BeautifulSoup object
		"""
		sauce = urllib.request.urlopen(url).read()
		return bs4.BeautifulSoup(sauce, 'lxml')
