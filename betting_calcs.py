import ods_calc as oc


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