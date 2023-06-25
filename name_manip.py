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
		}

	if name not in team_dict.keys():
		print(f'add ,{name}, to dictionary')
		new_name = name
	else:
		new_name = team_dict[name]
	return new_name