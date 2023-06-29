import ods_calc as oc
import file_man as fm


def add_stake(arbs: list, max_stake: int):
	"""
	finds out how much money you should bet on each team for an arbitrage bet
	:param arbs: the arbitrage opportunity
	:param max_stake: the max amount you want to put in
	:return: the arb list with the max amounts added
	"""
	for games in arbs:
		teams_ods = games[1]
		g1 = list(teams_ods[0])
		g2 = list(teams_ods[1])
		s1, s2 = oc.det_max_in(max_stake, oc.us_odd_to_prob(g1[-1]), oc.us_odd_to_prob(g2[-1]))
		g1.append(round(s1, 2))
		g2.append(round(s2, 2))
		games[1] = [tuple(g1), tuple(g2)]
	return arbs


def make_keys_set(dic: dict):
	"""
	makes the keys into a searchable item by splitting the keys into sets
	:param dic: the dictionary of the keys you want
	:return: the list of all the keys in set (and therefore searchable) form
	"""
	keys_lis = list(dic.keys())
	for i in range(len(keys_lis)):
		keys_lis[i] = set(keys_lis[i].split(','))
	return keys_lis


def arrange_odds(probs: dict, games: list[set]):
	"""
	arranges the odds
	:param probs: the team dictionary with odds
	:param games: the games being played
	:return arr_dic: the arranged dictionary {game: {site: odd}}
	"""
	keys_lis = None
	arr_dic = {}
	for game in games:
		time = [i for i in game if len(i) == 3][0]
		game.remove(time)
		n_key = ','.join(game) + ',' + time
		game.add(time)

		if keys_lis is None:
			keys_lis = make_keys_set(arr_dic)
		# if the key is not already created create a new one
		if set(n_key.split(',')) not in keys_lis:
			arr_dic[n_key] = {}

		# go through each key(which will be each site) and go through each team
		for key in probs.keys():
			for j in probs[key]:
				# split the club and the time
				club, day = j.split(',')
				if club in game and day in game:

					# check if the section of the dictionary has already been made
					f = False
					for r in keys_lis:
						if {club, day} <= r and club in arr_dic[n_key].keys():
							f = True

					# if it hasn't make a new one
					if f is False:
						arr_dic[n_key][club] = {}

					# add the probability in and update the key list
					arr_dic[n_key][club][key] = probs[key][j]
					keys_lis = make_keys_set(arr_dic)
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
				arr_odd[games][teams][sites] = oc.us_odd_to_prob(arr_odd[games][teams][sites])
	return arr_odd


def in_sort_arb_hl(data: list[list]):
	"""
	sorts data from a list of tuples from h to l. value assumed to be in -1th index
	:param data: unsorted list of tuple
	:return data: sorted list of tuples
	"""
	for idx in range(1, len(data)):
		while data[idx][-1] > data[idx - 1][-1] and idx > 0:
			temp = data[idx]
			data[idx] = data[idx - 1]
			data[idx - 1] = temp
			idx -= 1
	return data
