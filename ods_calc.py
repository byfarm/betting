def us_odd_to_prob(odd: int):
	# converts an int odd to probability
	if odd > 0:
		prob = 100 / (odd + 100)
	else:
		prob = abs(odd) / (abs(odd) + 100)
	return prob


def prob_to_dec_odds(prob: float):
	# converts a probability to decimal odds
	int_odd = 1 / prob
	return int_odd


def dec_odds_to_us_odds(odds: float):
	# converts decimal odds to us odds
	prob = 1 / odds
	us = prob_to_us_odds(prob)
	return us


def prob_to_us_odds(prob: float):
	# converts a probability to us odds
	try:
		if prob > 0.5:
			odd = -(-100 * prob) / (prob - 1)
		else:
			odd = (100 / prob) - 100
	except ZeroDivisionError:
		print(prob)
		odd = 0
	return int(odd)


def winnings_prob(prob: float, stake: float):
	# calculates the winnings based on probability
	winning = stake / prob
	return winning


def det_max_in(max_in: float, p1: float, p2: float):
	# determines each stake for a arbitrage bet
	stake2 = (p2 * max_in) / (p2 + p1)
	stake1 = max_in - stake2
	return stake1, stake2



