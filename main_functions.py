import scraping as sc
import file_man as fm
import betting_calcs as bc
import ods_calc as oc


def scrape_web():
	# initialize urls
	dk_url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'
	uni_url = "https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687638600154&useCombined=true&useCombinedLive=true"
	pin_url = 'https://www.pinnacle.com/en/baseball/mlb/matchups/#period:0'
	# scrape the websites
	dk, games_d = sc.scrape_dk_mlb(dk_url)
	uni, games_u = sc.scrape_unibet_mlb(uni_url)
	pin, games_p = sc.scrape_pin(pin_url)
	bfr, games_b = sc.scrape_betfair()
	'''
	# make sure each game is in both books
	if games_u != games_d:
		for i in games_d:
			if i not in games_u:
				games_d.remove(i)
		for i in games_u:
			if i not in games_d:
				games_u.remove(i)
	'''
	# write the odds and games to the txt file
	fm.write_new_table_dk_uni(games=games_u, DK_=dk, UNI=uni, PIN=pin, BFR=bfr)


def assemble_from_file():
	# read the odds and games from the txt file and arrange them
	odds, games = fm.read_from_file()
	p = bc.arrange_odds(odds, games)
	bc.arr_od_to_prob(p)
	return p


def find_arb(arr_prob: dict):
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
					p = oc.prob_to_us_lines(i)
					team_odds.append(p)
				teams_and_odds = list(zip(team_odds, teams, fs))
				opps.append([keys, teams_and_odds])
	return opps


def find_plus_ev(odds: dict[dict]):
	"""
	plan: calculate base prob from pinnicle or the market. then, calculate probabilities from everyone. sort based on % diff
	:return:
	"""
	plus_evs = []
	for game_k in odds.keys():
		game_dict = odds[game_k]
		for club_k in game_dict.keys():
			club_dict = game_dict[club_k]
			pin = 1
			bfr = 1
			if 'PIN' in club_dict.keys():
				pin = club_dict['PIN']
			if 'BFR' in club_dict.keys():
				bfr = club_dict['BFR']
			worst_case = min(pin, bfr)
			max_prob = 0
			web = None
			for site in club_dict.keys():
				prob = club_dict[site]
				if prob > max_prob:
					max_prob = prob
					web = site
			per_diff = round((max_prob - worst_case) * 100, 2)
			if per_diff > 0:
				max_odds = oc.prob_to_us_lines(max_prob)
				plus_evs.append([game_k, club_k, web, per_diff, max_odds])
	return plus_evs

