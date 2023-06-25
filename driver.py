if __name__ == '__main__':
	import file_man as fm
	import ods_calc as oc
	import scraping as sc
	import betting_calcs as bc

	max_stake = 100
	# initialize urls
	dk_url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'
	uni_url = "https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687638600154&useCombined=true&useCombinedLive=true"
	pin_url = 'https://www.pinnacle.com/en/baseball/mlb/matchups/#period:0'
	# scrape the websites
	dk, games_d = sc.scrape_dk_mlb(dk_url)
	uni, games_u = sc.scrape_unibet_mlb(uni_url)
	pin, games_p = sc.scrape_pin(pin_url)
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
	fm.write_new_table_dk_uni(dk, uni, pin, games_u)

	# read the odds and games from the txt file and arrange them
	odds, games = fm.read_from_file()
	p = bc.arrange_odds(odds, games)
	bc.arr_od_to_prob(p)

	# find arbitrage opportunities
	arbs = bc.find_arb(p)

	if len(arbs) > 0:
		results = bc.add_stake(arbs, max_stake)
		fm.write_results(results)
		print('New Results in!')
	else:
		print('No opportunities')
