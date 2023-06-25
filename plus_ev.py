

def calc_ev(prob: float, bet: float):
	"""
	calulates the expected value of a bet
	:param prob:
	:param bet:
	:return:
	"""
	odds = 1 / prob
	profit = bet * odds - bet
	ev = profit * prob - (1 - prob) * bet
	return ev