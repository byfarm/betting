from bs4 import BeautifulSoup
import requests
import datetime
import math


def allow_access(url):
	response = requests.get(url)
	return response.status_code


def scrape_dk_mlb(url):
	"""
	scrapes draftkings
	:param url: the url to draftkings mlb
	:return bet_list: the list of teams and their odds
	only can be used when no games are bing played
	"""
	response = requests.get(url).text
	soup = BeautifulSoup(response, 'html.parser')

	tbody = soup.tbody
	tbrs = tbody.contents

	bet_list = []
	for tr in tbrs:
		odds = tr.contents[3]
		odds_info = odds.div.span.string
		name = tr.contents[0]
		name_info = name.div.find('div', class_='event-cell__name-text').string

		# make the odds info able to convert to int
		lis = list(odds_info)
		if lis[0] != '+':
			lis[0] = '-'
		od = ''.join(lis)

		# append into the betting list
		betting = (name_info, int(od))
		bet_list.append(betting)

	games = []
	rn = math.floor(len(bet_list) / 2)
	for i in range(rn):
		t1 = bet_list[2*i][0]
		t2 = bet_list[2*i + 1][0]
		game = (t1, t2)
		games.append(set(game))

	return bet_list, games


def scrape_unibet_mlb(url):
	"""
	scraped the unibet mlb site for its betting data
	:param url: request url to the api, named matches.json?lan=en_US...
	'https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687557915663&useCombined=true&useCombinedLive=true'
	:return bet_list: the list of teams and their odds
	:return games: the set of games being played
	"""
	# get the json script
	response = requests.get(url).json()
	games = []
	bet_list = []
	for event in response['events']:
		try:
			state = event['event']['state']
			game_date = event['event']['start'][:10]
			# take all the games that have not started and is today
			if state[:3] == 'NOT' or len(state[:3]) == 3:
				# find the games, and their gamestate
				ht = event['event']['homeName']
				at = event['event']['awayName']
				game = (ht, at)
				games.append(set(game))

				# find the odds for each team in each game
				offers = event['betOffers'][0]
				for i in offers['outcomes']:
					name = i['label']
					od = int(i['oddsAmerican'])
					betting1 = (name, od)
					bet_list.append(betting1)
		except IndexError:
			pass

	return bet_list, games



