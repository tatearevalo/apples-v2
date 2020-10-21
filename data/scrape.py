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
	"""
	Apples-to-Apples web scraping class
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
		"""
		Scrape
		"""
		soup = self.red_soup if apples == 'red' else self.green_soup
		cards = []

		for li in soup.find_all('ul')[0]:
			card = self.create_card(li)
			if AppleScraper.is_card_valid(card):
				cards.append(card)

		return cards


	def create_card(self, li):
		"""
		Create a card from list item
		"""
		card = AppleScraper.default_card()

		if len(li) < 2:
			return card

		for item in li:
			# print(item)
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
		"""
		Add sets to the card
		"""
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
		"""
		is it valid?
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
		return re.sub(' - ', '', description)


	@staticmethod
	def url_to_soup(url):
		sauce = urllib.request.urlopen(url).read()
		return bs4.BeautifulSoup(sauce, 'lxml')
