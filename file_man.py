import scraping as sc
import datetime


def write_new_table_dk_uni(dk_mlb, uni_mlb):
	# open the problem file so you start at the end of it
	with open('live_odds.txt', 'w') as fp:
		fp.write(f'Betting odds as of {datetime.datetime.now()}\n')

		# write in the dk info
		fp.write('DK\n')
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
	return odds


