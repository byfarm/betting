from bs4 import BeautifulSoup
import requests
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ods_calc as oc
import name_manip as nm
import file_man as fm


def allow_access(url):
	response = requests.get(url)
	return response.status_code


def scrape_dk_mlb(url='https://sportsbook.draftkings.com/leagues/baseball/mlb'):
	"""
	scrapes draftkings
	:param url: the url to draftkings mlb
	:return bet_list: the list of teams and their odds
	only can be used when no games are bing played
	"""
	bet_list = []
	games = []
	response = requests.get(url)
	assert response.status_code == 200
	soup = BeautifulSoup(response.text, 'html.parser')

	tables = soup.find_all('table', class_='sportsbook-table')
	for table in tables:
		try:
			time = table.thead.tr.th.div.span.span.span.string[:3]
		except AttributeError:
			time = 'Tom'

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
			games.append(game)

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
	response = requests.get(url)
	assert response.status_code == 200
	response = response.json()
	games = []
	bet_list = []
	for event in response['events']:
		try:
			state = event['event']['state']
			game_date = event['event']['start'][:10]
			curr_date = datetime.datetime.now(datetime.timezone.utc)
			tom_date = curr_date + datetime.timedelta(days=1)
			av_dates = [str(curr_date)[:10], str(tom_date)[:10]]
			# take all the games that have not started and is today or tomorrow
			if state[:3] == 'NOT' and game_date in av_dates:
				if game_date == av_dates[0]:
					time = 'Tod'
				else:
					time = 'Tom'
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


def scrape_pin(url: str='https://www.pinnacle.com/en/baseball/mlb/matchups#period:0'):
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
		# find the day it says
		time = str(p.div.string)[:3]
		if time == 'Non':
			time = 'Tod'

		# find all the table rows with the teams and the odds
		tr = p.find_all('div', class_="style_row__21s9o style_row__21_Wa")
		for rows in tr:
			# find the teams and add to a list
			teams = rows.a.div.div.find_all('div', class_="ellipsis style_gameInfoLabel__24vcV")
			tm = [i.span.string for i in teams]

			# find the odds and add to a list
			buttons = rows.find_all('div', class_="style_button-wrapper__2pKZZ")
			odds = [i.button.span.string for i in buttons if i.button.span is not None]

			# if it is able to pull odds then send them
			if len(odds) > 0:
				for r in range(2):
					odds[r] = oc.int_odds_to_us(float(odds[r]))
					tm[r] = nm.cang_name(tm[r])
					go = [(tm[r], odds[r], time)]
					bet_list += go
				games.append(tuple(tm))
	return bet_list, games


def scrape_betfair(url='https://www.betfair.com.au/exchange/plus/baseball/competition/11196870'):
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
				d = tr.td.a.find('span', class_='label').text
				time = str(d)[:3]
				curr_date = datetime.datetime.now(datetime.timezone.utc).strftime('%A')[:3]
				if time == curr_date:
					time = 'Tod'
				elif time == 'Tom':
					time = 'Tom'
				else:
					time = 'Tod'

				# add to the bet list if all info there
				if len(odds) == 4 and len(teams) == 2 and time is not None:
					for r in range(2):
						mean_odd = (odds[2*r] + odds[(2 * r) + 1]) / 2
						odd_in = oc.int_odds_to_us(float(mean_odd))
						teams[r] = nm.cang_name(teams[r])
						go = [(teams[r], odd_in, str(time)[:3])]
						bet_list += go
					games.append(tuple(teams))
			except AttributeError:
				pass
	return bet_list, games
