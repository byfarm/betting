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


def scrape_dk_mlb(url='https://sportsbook.draftkings.com/leagues/baseball/mlb'):
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
	response = requests.get(url, headers=headers)
	assert response.status_code == 200
	soup = BeautifulSoup(response.text, 'html.parser')
	tlist = []
	tables = soup.find_all('table', class_='sportsbook-table')
	for table in tables:

		try:
			time = table.thead.tr.th.div.span.span.span.string[:3]
		except AttributeError:
			time = 'LIV'
		tlist.append(time)

		tbrs = table.tbody.contents
		for tr in tbrs:
			try:
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
				betting = (name_info, int(od), time)
				bet_list.append(betting)
			except AttributeError:
				pass

		rn = len(bet_list) // 2
		for i in range(rn):
			t1 = bet_list[2*i][0]
			t2 = bet_list[2*i + 1][0]
			game = (t1, t2, time)
			in_ = False
			for p in range(len(tlist)):
				c_game = (game[0], game[1], tlist[p])
				if c_game in games:
					in_ = True
			if not in_:
				games.append(game)

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
				game_date = event['event']['start'][:10]
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
	wait = WebDriverWait(driver, 5)
	wait.until(EC.presence_of_element_located((By.CLASS_NAME, "style_price__3LrWW")))

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
		trs = p.find_all('div', class_="style_row__21s9o style_row__21_Wa")

		for rows in trs:
			# find the teams and add to a list
			teams = rows.a.div.div.find_all('div', class_="ellipsis style_gameInfoLabel__24vcV")
			tm = [nm.cang_name(i.span.string) for i in teams]

			# find the odds and add to a list
			buttons = rows.find_all('div', class_="style_button-wrapper__2pKZZ")
			odds = [oc.dec_odds_to_us_odds(float(i.button.span.string)) for i in buttons if i.button.span is not None]
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
	wait.until(EC.presence_of_element_located((By.CLASS_NAME, "name")))

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
		game_date = event['startsAt'][:10]
		time = nm.find_start_time(game_date)

		gms = []
		info = event['specialFixedOddsMarkets'][0]['outcomes']
		for i in info:
			team = i['name']
			team = nm.cang_name(team)
			dec_odds = i['price']
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
			s_time = event['startTime'][:10]
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
			s_time = response['attachments']['events'][str(event_id)]['openDate'][:10]
			time = nm.find_start_time(s_time)

			gms = []
			contenders = market['runners']
			for side in contenders:
				team = side['nameAbbr']
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
			assert info['name'] == 'Money Line'

			gms = set()
			betting = []
			for i in info['selection']:
				team = nm.cang_name(i['name'])
				odds = oc.dec_odds_to_us_odds(float(i['odds']['dec']))
				gms.add(team)
				betting.append([team, odds])

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


