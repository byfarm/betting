def odd_to_prob(odd: int):
	# converts an int odd to probability
	if odd > 0:
		prob = 100 / (odd + 100)
	else:
		prob = abs(odd) / (abs(odd) + 100)
	return prob

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
	for games in arr_odd.keys():
		for teams in arr_odd[games].keys():
			for sites in arr_odd[games][teams]:
				arr_odd[games][teams][sites] = odd_to_prob(arr_odd[games][teams][sites])

	print()

