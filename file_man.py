import scraping as sc
import datetime


def write_new_table_dk_uni(dk_mlb: tuple, uni_mlb: tuple, games: set):
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
		# write in the dk info
		fp.write('\nDK\n')
		for i in range(len(dk_mlb)):
			team = str(dk_mlb[i][0])
			odds = str(dk_mlb[i][1])
			fp.write(team + ',' + odds + '\n')

		# write in the uni info
		fp.write('UNI\n')
		for i in range(len(uni_mlb)):
			team = str(uni_mlb[i][0])
			odds = str(uni_mlb[i][1])
			fp.write(team + ',' + odds + '\n')
		fp.write('')


def read_from_file():
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
				team, od = line.split(',')
				odds[site][team] = int(od)
			line = fp.readline().strip()
	return odds, games


def write_results(arbs: list):
	with open('results.txt', 'w') as fp:
		fp.write(f'arbitrage opportunities as of {datetime.datetime.now()}\n')
		for opps in arbs:
			t_and_o = opps[1]
			g1 = t_and_o[0]
			g2 = t_and_o[1]
			fp.write(f'{opps[0]}:\n')
			fp.write(f'{g1}\n')
			fp.write(f'{g2}\n\n')

