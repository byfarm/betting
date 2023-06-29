import scraping as sc
import file_man as fm
import betting_calcs as bc
import ods_calc as oc


def scrape_web():
	"""
	scrapes the websites for all of their betting info and writes it to a txt file
	"""
	# scrape the websites
	uni, games_uni = sc.scrape_unibet_mlb()
	dk, games_dk = sc.scrape_dk_mlb()
	pin, games_pin = sc.scrape_pin(games_uni)
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
	for key in arr_prob.keys():
		game = arr_prob[key]

		best_p = []
		best_s = []
		teams = list(game.keys())
		for team in game.keys():
			team_prob = game[team]
			sites = list(team_prob.keys())
			min_p = 1
			i_site = None
			for site in sites:
				if team_prob[site] < min_p:
					min_p = team_prob[site]
					i_site = site
			best_p.append(min_p)
			best_s.append(i_site)

		if sum(best_p) < 1:
			for i in range(len(best_p)):
				best_p[i] = oc.prob_to_us_odds(best_p[i])
			od_and_prob = list(zip(teams, best_s, best_p))
			opps.append([key, od_and_prob])

	for op in opps:
		t_and_o = op[1]
		tot_advantage = []
		for f in range(len(t_and_o)):
			g1 = t_and_o[f]
			tot_advantage.append(oc.us_odd_to_prob(g1[-1]) * 100)
		op.append(round(100 - sum(tot_advantage), 2))
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

