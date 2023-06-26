import name_manip as nm
import scraping as sc
import datetime


def write_new_table_dk_uni(games: set, **kwargs):
	"""
	writes the odds and games to a txt file
	:param dk_mlb: (team, odds)
	:param uni_mlb: (team, odds)
	:param games: all the games going on
	:return: a new txt file
	"""
	# open the problem file so you start at the end of it
	with open('live_odds.txt', 'w') as fp:
		# write the header and all the games
		fp.write(f'Betting odds as of {datetime.datetime.now()}\n')
		for i in games:
			fp.write(f'{i}:')
		fp.write('\n')

		for key in kwargs.keys():
			# write in the dk info
			fp.write(f'{key}\n')
			for i in range(len(kwargs[key])):
				team = str(kwargs[key][i][0])
				odds = str(kwargs[key][i][1])
				time = str(kwargs[key][i][2])
				fp.write(team + ',' + odds + ',' + time + '\n')
		fp.write('')


def read_from_live_odds():
	"""
	reads from the live odds file
	:return odds: dictionary , like the one that was read in
	:return games: list , all the games that are being played
	"""
	odds = {}
	with open('live_odds.txt', 'r') as fp:
		# open and skip first line
		fp.readline()

		# reformat the games
		games = fp.readline().strip().split(':')[:-1]
		for i in range(len(games)):
			games[i] = games[i][1:-1].replace("'", "").split(', ')
		for q in range(len(games)):
			games[q] = set(games[q])

		# find the first site and make it a closed dic
		line = fp.readline().strip()
		while line != '':
			# if it is a header then add it to an empty set in the dictioanry
			if len(line) <= 3:
				site = line
				odds[site] = {}
			else:
				# if data split it and add to dictionary
				team, od, time = line.split(',')
				odds[site][team + ',' + time] = int(od)
			line = fp.readline().strip()
	return odds, games


def write_results(arbs: list):
	"""
	writes the arbitage results to a txt file
	:param arbs: the arbitrage results
	:return: a new txt file
	"""
	with open('results.txt', 'w') as fp:
		fp.write(f'arbitrage opportunities as of {datetime.datetime.now()}\n')
		for opps in arbs:
			t_and_o = opps[1]
			g1 = t_and_o[0]
			g2 = t_and_o[1]
			fp.write(f'{opps[0]}:\n')
			fp.write(f'{g1}\n')
			fp.write(f'{g2}\n\n')


def write_plus_ev(evs: list):
	"""
	writes the plus ev opportunities to a txt
	:param evs: a sorted list of all the ev opportunities
	:return: a new txt file
	"""
	with open('plus_ev_opps.txt', 'w') as fp:
		fp.write(f'Plus EV opportunities as of {datetime.datetime.now()}\n')
		for opps in evs:
			fp.write(f'\nGame: {opps[0]}, Club: {opps[1]}, Website: {nm.sites_dict(opps[2])}\n')
			fp.write(f'{opps[3]}%, Width: {opps[4]} cents, Real Odds: {opps[5]}, {opps[2]} Odds: {opps[6]}\n')
		fp.write('')


