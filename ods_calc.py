
def odds_to_prob(odds: dict):
	for i in odds.keys():
		if odds[i] > 0:
			odds[i] = 100 / (odds[i] + 100)
		else:
			odds[i] = abs(odds[i]) / (abs(odds[i]) + 100)
	return odds