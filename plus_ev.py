

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


def insert_sort_h_to_l(data: list[list]):
	"""
	sorts data from a list of tuples from h to l. value assumed to be in 0th index of tuple
	:param data: unsorted list of tuple
	:return data: sorted list of tuples
	"""
	for idx in range(1, len(data)):
		while data[idx][-4] > data[idx - 1][-4] and idx > 0:
			temp = data[idx]
			data[idx] = data[idx - 1]
			data[idx - 1] = temp
			idx -= 1
	return data