import datetime


def cang_name(name: str):
	"""
	changes the full name to the abreviated name
	:param name: full name of the team
	:return: the abreviated name
	"""
	team_dict = {
		'Minnesota Twins': 'MIN Twins',
		'Detroit Tigers': 'DET Tigers',
		'Los Angeles Dodgers': 'LA Dodgers',
		'Houston Astros': 'HOU Astros',
		'Washington Nationals': 'WAS Nationals',
		'San Diego Padres': 'SD Padres',
		'Colorado Rockies': 'COL Rockies',
		'Los Angeles Angels': 'LA Angels',
		'New York Yankees': 'NY Yankees',
		'Texas Rangers': 'TEX Rangers',
		'Philadelphia Phillies': 'PHI Phillies',
		'New York Mets': 'NY Mets',
		'Oakland Athletics': 'OAK Athletics',
		'Toronto Blue Jays': 'TOR Blue Jays',
		'Miami Marlins': 'MIA Marlins',
		'Pittsburgh Pirates': 'PIT Pirates',
		'Tampa Bay Rays': 'TB Rays',
		'Kansas City Royals': 'KC Royals',
		'Cleveland Guardians': 'CLE Guardians',
		'Milwaukee Brewers': 'MIL Brewers',
		'San Francisco Giants': 'SF Giants',
		'Arizona Diamondbacks': 'ARI Diamondbacks',
		'Chicago Cubs': 'CHI Cubs',
		'St. Louis Cardinals': 'STL Cardinals',
		'Seattle Mariners': 'SEA Mariners',
		'Baltimore Orioles': 'BAL Orioles',
		'Atlanta Braves': 'ATL Braves',
		'Cincinnati Reds': 'CIN Reds',
		'Boston Red Sox': 'BOS Red Sox',
		'Chicago White Sox': 'CHI White Sox'
		}

	if name not in team_dict.keys():
		print(f'add ,{name}, to dictionary')
	else:
		name = team_dict[name]
	return name


def find_start_time(start):
	"""
	finds the start time of the event
	:param start: the utc start time of the event
	:return time: str , either tod, tom, or n/a
	"""
	start = str(start)[:10]
	curr_date = datetime.datetime.now(datetime.timezone.utc)
	tom_date = curr_date + datetime.timedelta(days=1)
	liv_date = curr_date - datetime.timedelta(days=1)
	av_dates = [str(liv_date)[:10], str(curr_date)[:10], str(tom_date)[:10]]
	if start in av_dates:
		if start == av_dates[1]:
			time = 'Tod'
		elif start == av_dates[2]:
			time = 'Tom'
		else:
			time = 'LIV'
	else:
		time = 'N/A'
	return time


def sites_dict(abriv: str):
	"""
	changed from the abriviated site name to the full name
	:param abriv: abriviated site name
	:return: the full site name
	"""
	sites = {
		'DK_': 'Draft Kings',
		'UNI':	'UniBet',
		'PIN':	'Pinnacle',
		'PB_': 'Points Bet',
		'CSB': 'Caeser',
		'FD_': 'Fan Duel',
		'FOX': 'Fox Bets'
	}
	return sites[abriv]