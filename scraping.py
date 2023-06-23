from bs4 import BeautifulSoup
import requests

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

def scrape_bet365_mlb(url):
	response = requests.get(url).text
	print(response)


url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'
r = scrape_dk_mlb(url)
print(r)



