from bs4 import BeautifulSoup
import requests
import datetime
import copy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ods_calc as oc
import name_manip as nm


def allow_access(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
	}
	response = requests.get(url, headers=headers)
	status_code = response.status_code
	return status_code


def scrape_dk_mlb(games_lis, url='https://sportsbook.draftkings.com/leagues/baseball/mlb'):
	"""
	scrapes draftkings, type: directly from website, chromedriver not required
	:param url: the url to draftkings mlb
	:return bet_list: the list of teams and their odds
	only can be used when no games are bing played
	"""
	bet_list = []
	games = []
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
	}

	# make the cl copy searchable
	e_copy_gl = copy.deepcopy(games_lis)
	copy_gl = copy.deepcopy(games_lis)
	for p in range(len(copy_gl)):
		copy_gl[p] = list(({copy_gl[p][0], copy_gl[p][1]}, copy_gl[p][2]))

	response = requests.get(url, headers=headers)
	assert response.status_code == 200
	soup = BeautifulSoup(response.text, 'html.parser')
	tables = soup.find_all('table', class_='sportsbook-table')

	for table in tables:
		tbrs = table.tbody.contents
		for tr in tbrs:
			try:
				odds = tr.contents[3].div.span.string
				name = tr.contents[0].div.find('div', class_='event-cell__name-text').string

				# make the odds info able to convert to int
				lis = list(odds)
				if lis[0] != '+':
					lis[0] = '-'
				od = ''.join(lis)

				# append into the betting list
				bet_list.append([name, int(od)])
			except AttributeError:
				pass

	# add the times in
	for i in range(len(bet_list)//2):
		gms = {bet_list[2*i][0], bet_list[2*i+1][0]}
		for t in range(len(copy_gl)):
			if len(copy_gl[t]) > 0:
				a_game = copy_gl[t][0]
				if gms == a_game:
					game = copy.deepcopy(e_copy_gl[t])
					bet_list[2*i] += [game[-1]]
					bet_list[2*i+1] += [game[-1]]
					games.append(game)
					copy_gl[t] = []
					e_copy_gl[t] = []

	# remove all elements from the betting list
	r_list = []
	for g in bet_list:
		if len(g) != 3:
			r_list.append(g)
	for r in r_list:
		bet_list.remove(r)

	return bet_list, games


def scrape_unibet_mlb(url='https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687638600154&useCombined=true&useCombinedLive=true'):
	"""
	scraped the unibet mlb site for its betting data, type: reads a json file with all the betting info
	:param url: request url to the api, named matches.json?lan=en_US...
	'https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687557915663&useCombined=true&useCombinedLive=true'
	:return bet_list: the list of teams and their odds
	:return games: the set of games being played
	"""
	# get the json script
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
	}
	response = requests.get(url, headers=headers)
	assert response.status_code == 200
	response = response.json()
	games = []
	bet_list = []
	for event in response['events']:
		try:
			if event['event']['state'][:3] == 'NOT':
				game_date = event['event']['start']
				time = nm.find_start_time(game_date)
			else:
				time = 'LIV'
			# find the games, and their gamestate
			ht = event['event']['homeName']
			at = event['event']['awayName']
			game = (ht, at, time)
			games.append(game)

			# find the odds for each team in each game
			offers = event['betOffers'][0]
			for i in offers['outcomes']:
				name = i['label']
				od = int(i['oddsAmerican'])
				betting1 = (name, od, time)
				bet_list.append(betting1)
		except IndexError:
			pass

	return bet_list, games


def scrape_pin(games_lis, url='https://www.pinnacle.com/en/baseball/mlb/matchups#period:0'):
	""" scrapes pinnacle sportsbook. type: read directly from website """
	# make the cl copy searchable
	e_copy_gl = copy.deepcopy(games_lis)
	copy_gl = copy.deepcopy(games_lis)
	for p in range(len(copy_gl)):
		copy_gl[p] = list(({copy_gl[p][0], copy_gl[p][1]}, copy_gl[p][2]))

	bet_list = []
	games = []
	# Configure Chrome options
	chrome_options = Options()
	chrome_options.add_argument("--headless")  # Run Chrome in headless mode

	# Initialize Chrome WebDriver
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(url)

	# Wait for the content to load (adjust the timeout as needed)
	wait = WebDriverWait(driver, 10)
	wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mb")))

	# Get the page source after JavaScript rendering
	page_source = driver.page_source

	# Create a BeautifulSoup object to parse the HTML
	soup = BeautifulSoup(page_source, "html.parser")

	# Close the WebDriver
	driver.quit()

	# find all the table headers
	headers = soup.find_all('div', class_='contentBlock square')
	for p in headers:
		# find all the table rows with the teams and the odds
		trs = p.contents[2:]

		for rows in trs:
			# find the teams and add to a list

			teams = rows.find_all("span", class_="ellipsis event-row-participant style_participant__1W3B4")
			tm = [nm.cang_name(i.text) for i in teams]

			# find the odds and add to a list
			buttons = rows.find_all('span', class_="style_price__1-7o_")
			odds = [oc.dec_odds_to_us_odds(float(i.text)) for i in buttons if i.text is not None and float(i.text) > 1]
			betting = [[tm[0], odds[0]], [tm[1], odds[1]]]
			tm = set(tm)

			for idx in range(len(copy_gl)):
				games_t = copy_gl[idx][0]
				if tm == games_t and copy_gl[idx][-1] != 'LIV':
					game = e_copy_gl[idx]
					del copy_gl[idx]
					del e_copy_gl[idx]
					games.append(game)
					for bets in betting:
						bets.append(game[-1])
						bet_list.append(bets)
					break

	return bet_list, games


def scrape_betfair(url='https://www.betfair.com.au/exchange/plus/baseball/competition/11196870'):
	""" scrapes betfair, type: read directly from website"""
	# Configure Chrome options
	chrome_options = Options()
	chrome_options.add_argument("--headless")  # Run Chrome in headless mode

	# Initialize Chrome WebDriver
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(url)

	# Wait for the content to load (adjust the timeout as needed)
	wait = WebDriverWait(driver, 5)
	wait.until(EC.presence_of_element_located((By.CLASS_NAME, "section")))

	# Get the page source after JavaScript rendering
	page_source = driver.page_source

	# Create a BeautifulSoup object to parse the HTML
	soup = BeautifulSoup(page_source, "html.parser")
	driver.quit()

	bet_list = []
	games = []

	tables = soup.find_all('div', class_='coupon-table-mod')
	for table in tables:
		tbrs = table.tbody.contents
		for tr in tbrs:
			try:
				# get the teams
				t = tr.td.a.find('ul', class_='runners').contents
				teams = [i.contents[0] for i in t]

				# get the odds
				o = str(tr.find('td', class_='coupon-runners').text)
				r = o.split('\n')
				odds = [float(i) for i in r if i != '' and i[0] != '$']

				# get the day
				d = tr.td.a.find('div', class_='start-date-wrapper').span.text
				time = str(d)[:3]
				curr_date = datetime.datetime.now(datetime.timezone.utc).strftime('%A')[:3]
				if time == 'I18':
					time = 'Tod'
				elif time != curr_date:
					time = 'Tom'
				# add to the bet list if all info there
				if len(odds) == 4 and len(teams) == 2 and time is not None:
					for r in range(2):
						mean_odd = (odds[2*r] + odds[(2 * r) + 1]) / 2
						odd_in = oc.dec_odds_to_us_odds(float(mean_odd))
						teams[r] = nm.cang_name(teams[r])
						go = [(teams[r], odd_in, str(time)[:3])]
						bet_list += go
					games.append((teams[0], teams[1], str(time)[:3]))
			except AttributeError:
				pass
	return bet_list, games


def scrape_pointsbet(url='https://api.co.pointsbet.com/api/v2/competitions/6535/events/featured?includeLive=false&page=1'):
	''' scrapes pointsbet website, type: scrapes a json file'''
	# get the json script
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
	}
	response = requests.get(url, headers=headers)
	assert response.status_code == 200
	response = response.json()
	games = []
	bet_list = []
	for event in response['events']:
		# find the time
		if event['isLive'] is True:
			time = 'LIV'
		else:
			game_date = event['startsAt']
			time = nm.find_start_time(game_date)

		gms = []
		info = event['specialFixedOddsMarkets'][0]['outcomes']
		for i in info:
			team = i['name']
			team = nm.cang_name(team)
			dec_odds = i['price']
			if dec_odds > 1:
				usa_odds = oc.dec_odds_to_us_odds(dec_odds)
				betting = (team, usa_odds, time)
				bet_list.append(betting)
				gms.append(team)
		games.append(tuple(gms + [time]))
	return bet_list, games


def scrape_CSP(url='https://api.americanwagering.com/regions/us/locations/co/brands/czr/sb/v3/sports/baseball/events/schedule/?competitionIds=04f90892-3afa-4e84-acce-5b89f151063d'):
	'''scrapes from caesers sportsbook, type: reads json file'''
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
	}
	response = requests.get(url, headers=headers)
	assert response.status_code == 200
	response = response.json()

	games = []
	bet_list = []
	for event in response['competitions'][0]['events']:
		if len(event['markets']) > 0:
			# find what time the game is
			s_time = event['startTime']
			time = nm.find_start_time(s_time)

			# find the team and odds
			gms = []

			info = event['markets'][0]
			if info['displayName'] == 'Money Line':
				for i in info['selections']:
					team = nm.cang_name(i['name'][1:-1])
					odds = i['price']['a']
					betting = (team, odds, time)
					bet_list.append(betting)
					gms.append(team)
				games.append(tuple(gms + [time]))
	return bet_list, games


def scrape_FD_(url='https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=mlb&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York'):
	'''scrapes fanduel website, type: reads a json file'''
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
	}
	response = requests.get(url, headers=headers)
	assert response.status_code == 200
	response = response.json()
	bet_list = []
	games = []
	markets = response['attachments']['markets']
	for market in markets.values():
		if market['marketType'] == 'MONEY_LINE' and market['numberOfRunners'] == 2:
			# find the time
			event_id = market['eventId']
			if market['inPlay'] is True:
				time = 'LIV'
			else:
				s_time = response['attachments']['events'][str(event_id)]['openDate']
				time = nm.find_start_time(s_time)

			gms = []
			contenders = market['runners']
			for side in contenders:
				try:
					team = side['nameAbbr']
				except KeyError:
					team = side["runnerName"]
					team = nm.cang_name(team)
				odds = side['winRunnerOdds']['americanDisplayOdds']['americanOdds']
				betting = (team, odds, time)
				bet_list.append(betting)
				gms.append(team)
			games.append(tuple(gms + [time]))
	return bet_list, games


def scrape_FOX(games_lis, url='https://sports.co.foxbet.com/sportsbook/v1/api/getCompetitionEvents?competitionId=8661882&marketTypes=BBPS%2CBASEBALL%3AFTOT%3AAHCP_MAIN%2CBBML%2CBASEBALL%3AFTOT%3AML%2CBBTS%2CBASEBALL%3AFTOT%3AOU_MAIN&includeOutrights=false&skip=0&take=20&channelId=17&locale=en-us&siteId=536870914'):
	"""
	scrapes fox betting using a json file. needs game list to find the time of each game
	:param games_lis: an imported games list from a different scrape
	:param url: link to fox
	:return: bet_list, games
	"""
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
	}
	response = requests.get(url, headers=headers)
	assert response.status_code == 200
	response = response.json()

	# make the cl copy searchable
	e_copy_gl = copy.deepcopy(games_lis)
	copy_gl = copy.deepcopy(games_lis)
	for p in range(len(copy_gl)):
		copy_gl[p] = list(({copy_gl[p][0], copy_gl[p][1]}, copy_gl[p][2]))

	events = response['event']
	bet_list = []
	games = []
	for event in events:
		if len(event['markets']) == 3:
			info = event['markets'][2]
			if info['name'] == 'Money Line':

				gms = set()
				betting = []
				for i in info['selection']:
					try:
						team = nm.cang_name(i['name'])
						odds = float(i['odds']['dec'])
						if odds > 1:
							odds = oc.dec_odds_to_us_odds(odds)
							gms.add(team)
							betting.append([team, odds])
					except ValueError:
						pass

				for idx in range(len(copy_gl)):
					games_t = copy_gl[idx][0]
					if gms == games_t:
						game = e_copy_gl[idx]
						del copy_gl[idx]
						del e_copy_gl[idx]
						games.append(game)
						for bets in betting:
							bets.append(game[-1])
							bet_list.append(bets)
						break
	return bet_list, games


def scrape_betrivers(url="https://eu-offering-api.kambicdn.com/offering/v2018/rsi2uspa/event/live/open.json?lang=en_US&market=US-PA&client_id=2&channel_id=1&ncid=1689643196188"):
	# type is api
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
	}
	response = requests.get(url, headers=headers)
	assert response.status_code == 200
	response = response.json()

	bet_list = []
	games = []
	for gm in response['liveEvents']:
		try:
			info = gm["mainBetOffer"]
			if info['criterion']['label'] == 'Moneyline' and gm['event']['group'] == "MLB":
				time = gm["event"]['start']
				time = nm.find_start_time(time)
				tms = [team['label'] for team in info['outcomes']]
				odds = [int(team['oddsAmerican']) for team in info['outcomes']]
				bet_list.append([tms[0], odds[0], time])
				bet_list.append([tms[1], odds[1], time])
				games.append((tms[0], tms[1], time))
		except KeyError:
			pass
	return bet_list, games



