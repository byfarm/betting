import scraping as sc
import file_man as fm
import betting_calcs as bc
import ods_calc as oc


def scrape_web():
	"""
	scrapes the websites for all of their betting info and writes it to a txt file
	"""
	# scrape the websites
	dk, games_dk = sc.scrape_dk_mlb()
	uni, games_uni = sc.scrape_unibet_mlb()
	pin, games_pin = sc.scrape_pin()
	pb, games_pb = sc.scrape_pointsbet()
	csb, games_csb = sc.scrape_CSP()
	fd, games_fd = sc.scrape_FD_()
	fox, games_fox = sc.scrape_FOX(games_uni)
	#bfr, games_b = sc.scrape_betfair()
	# write the odds and games to the txt file
	fm.write_new_table_dk_uni(games=games_uni, DK_=dk, UNI=uni, PIN=pin, PB_=pb, CSB=csb, FD_=fd, FOX=fox)


def assemble_from_file():
	'''
	assembles all the data from the txt file
	:return:
	'''
	# read the odds and games from the txt file and arrange them
	odds, games = fm.read_from_live_odds()
	game_dict = bc.arrange_odds(odds, games)
	bc.arr_od_to_prob(game_dict)
	return game_dict, odds, games


def find_arb(arr_prob: dict):
	"""
	goes through the game dict of probs and find arbitrage opportunities
	:param arr_prob: the dictionary with the games at the highest level and the sites at the second lowest
	:return: list of arbitrage opportunities
	"""
	# the list of opportunities
	opps = []

	# navigate to the probibilites while saving important info
	for keys in arr_prob.keys():
		game = arr_prob[keys]
		teams = list(game.keys())
		for team in game.values():
			sites = list(team.keys())
			sum_prob = []
			fs = []
			for club in teams:
				mp = game[club][sites[0]]
				site = sites[0]

				# find the max probability and add into the list
				for i in range(1, len(sites)):
					if sites[i] in game[club].keys():
						p2 = game[club][sites[i]]
						if p2 > mp:
							mp = p2
							site = sites[i]
				sum_prob.append(mp)
				fs.append(site)
			# if the sum of the list is less than 1 then there is an arbitrage opportunity
			if sum(sum_prob) < 1:
				team_odds = []
				for i in sum_prob:
					p = oc.prob_to_us_odds(i)
					team_odds.append(p)
				teams_and_odds = list(zip(team_odds, teams, fs))
				opps.append([keys, teams_and_odds])
	return opps


def find_plus_ev(odds: dict[dict]):
	"""
	calculate base prob from pinnicle or the market. then, calculate probabilities from everyone. sort based on % diff
	:return plus_evs: a list of all the plus ev betts
	"""
	plus_evs = []
	for game_k in odds.keys():
		game_dict = odds[game_k]

		# find the width from the accurate bookie
		t_play = list(game_dict.keys())
		acc_books = ['BFR', 'PIN']
		width = None

		# go through each team and make sure the accurate bookie is in both
		for book in acc_books:
			r = game_dict[t_play[0]].keys()
			p = game_dict[t_play[1]].keys()
			if book in r and book in p:

				# if true change the probs to US and find the width
				t1 = oc.prob_to_us_odds(game_dict[t_play[0]][book])
				t2 = oc.prob_to_us_odds(game_dict[t_play[1]][book])
				if t1 < 0 and t2 < 0:
					t1 = int(str(t1)[-2:])
					t2 = int(str(t2)[-2:])
					width = abs(t1 + t2)
				else:
					width = abs(t1 + t2)

		# if valid, see if it is a plus ev bet
		if width is not None:
			for club_k in game_dict.keys():

				# find the worst case out of the two good bookies
				club_dict = game_dict[club_k]
				pin = 1
				bfr = 1
				if 'PIN' in club_dict.keys():
					pin = club_dict['PIN']
				if 'BFR' in club_dict.keys():
					bfr = club_dict['BFR']
				worst_case = min(pin, bfr)

				# find the max probability and the website corresponding to it
				max_prob = 0
				web = None
				for site in club_dict.keys():
					prob = club_dict[site]
					if prob > max_prob:
						max_prob = prob
						web = site

				# find the percent difference and if it is greater than 0 then it is a plus ev bet
				per_diff = round((max_prob - worst_case) * 100, 2)
				if per_diff > 0:
					max_odds = oc.prob_to_us_odds(max_prob)
					real_odds = oc.prob_to_us_odds(worst_case)
					plus_evs.append([game_k, club_k, web, per_diff, width, real_odds, max_odds])

	return plus_evs

