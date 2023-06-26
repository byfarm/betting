import datetime


def cang_name(name: str):
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
		'Boston Red Sox': 'BOS Red Socks',
		'Chicago White Sox': 'CHI White Socks'
		}

	if name not in team_dict.keys():
		print(f'add ,{name}, to dictionary')
		new_name = name
	else:
		new_name = team_dict[name]
	return new_name


def find_start_time(start):
	start = start[:10]
	curr_date = datetime.datetime.now(datetime.timezone.utc)
	tom_date = curr_date + datetime.timedelta(days=1)
	av_dates = [str(curr_date)[:10], str(tom_date)[:10]]
	if start in av_dates:
		if start == av_dates[0]:
			time = 'Tod'
		else:
			time = 'Tom'
	else:
		time = 'N/A'
	return time
