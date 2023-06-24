def odd_to_prob(odd: int):
	# converts an int odd to probability
	if odd > 0:
		prob = 100 / (odd + 100)
	else:
		prob = abs(odd) / (abs(odd) + 100)
	return prob


def prob_to_int_odds(prob: float):
	int_odd = 1 / prob
	return int_odd


def int_odds_to_us(odds: float):
	prob = 1 / odds
	us = prob_to_us_lines(prob)
	return us


def prob_to_us_lines(prob: float):
	if prob > 0.5:
		odd = -(-100 * prob) / (prob - 1)
	else:
		odd = (100 / prob) - 100
	return int(odd)


def winnings_prob(prob: float, stake: float):
	winning = stake / prob
	return winning


def det_max_in(max_in: float, p1: float, p2: float):
	stake2 = (p2 * max_in) / (p2 + p1)
	stake1 = max_in - stake2
	return stake1, stake2


def arrange_odds(probs: dict, games: list[set]):
	"""
	arranges the odds
	:param probs: the team dictionary with odds
	:param games: the games being played
	:return arr_dic: the arranged dictionary {game: {site: odd}}
	"""
	arr_dic = {}
	for game in games:
		n_key = ','.join(game)

		# if the key is not already created create a new one
		if n_key not in arr_dic.keys():
			arr_dic[n_key] = {}

		# go through each key(which will be each site) and go through each team
		for key in probs.keys():
			for i in probs[key]:
				if i in game:
					if i not in arr_dic[n_key].keys():
						arr_dic[n_key][i] = {}
					arr_dic[n_key][i][key] = probs[key][i]
	return arr_dic


def arr_od_to_prob(arr_odd: dict):
	"""
	changes the arranged odds to arranged probabilites
	:param arr_odd:
	:return: updates the input
	"""
	for games in arr_odd.keys():
		for teams in arr_odd[games].keys():
			for sites in arr_odd[games][teams]:
				arr_odd[games][teams][sites] = odd_to_prob(arr_odd[games][teams][sites])
	return arr_odd


def find_arb(arr_prob: dict):
	site = None
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
					p = prob_to_us_lines(i)
					team_odds.append(p)
				teams_and_odds = list(zip(team_odds, teams, fs))
				opps.append([keys, teams_and_odds])
	return opps
