from bs4 import BeautifulSoup
import requests


def allow_access(url):
	response = requests.get(url)
	print(response.status_code)


def scrape_dk_mlb(url):
	""""""
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

	return bet_list


def scrape_unibet_mlb(url):
	"""
	scraped the unibet mlb site for its betting data
	:param url: request url to the api, named matches.json?lan=en_US...
	'https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687557915663&useCombined=true&useCombinedLive=true'
	:return bet_list: the list of teams and their odds
	"""

	response = requests.get(url).json()

	bet_list = []
	for event in response['events']:
		offers = event['betOffers'][0]
		outcomes = offers['outcomes'][0]
		name = outcomes['label']
		od = int(outcomes['oddsAmerican'])
		betting = (name, od)
		bet_list.append(betting)

	return bet_list


url = 'https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687557915663&useCombined=true&useCombinedLive=true'
r = scrape_unibet_mlb(url)
print(r)



