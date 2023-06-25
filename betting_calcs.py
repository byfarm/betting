import ods_calc as oc
import file_man as fm


def add_stake(arbs: list, max_stake: int):
	for games in arbs:
		teams_ods = games[1]
		g1 = list(teams_ods[0])
		g2 = list(teams_ods[1])
		p1 = oc.odd_to_prob(g1[0])
		p2 = oc.odd_to_prob(g2[0])
		s1, s2 = oc.det_max_in(max_stake, p1, p2)
		g1.append(round(s1, 2))
		g2.append(round(s2, 2))
		games[1] = [tuple(g1), tuple(g2)]
	return arbs

def make_keys_list(dic: dict):
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
			keys_lis = make_keys_list(arr_dic)
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
					keys_lis = make_keys_list(arr_dic)
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
				arr_odd[games][teams][sites] = oc.odd_to_prob(arr_odd[games][teams][sites])
	return arr_odd


