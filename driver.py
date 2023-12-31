if __name__ == '__main__':
	import file_man as fm
	import betting_calcs as bc
	import main_functions as mf
	import plus_ev as pe

	# set the maximum you want to bet
	max_stake = 100

	# scrape the websites for their betting info
	mf.scrape_web()

	# read everything from the file
	game_dict, site_dict, games = mf.assemble_from_file()

	# find ev opportunities
	evs = mf.find_plus_ev(game_dict)
	sort_evs = pe.in_sort_ev_hl(evs)

	if len(sort_evs) > 0:
		print(f'\nTop EV: {sort_evs[0]}')
		fm.write_plus_ev(sort_evs)
	else:
		print('\nNo EVs')

	# find arbitrage opportunities
	arbs = mf.find_arb(game_dict)

	if len(arbs) > 0:
		bc.in_sort_arb_hl(arbs)
		results = bc.add_stake(arbs, max_stake)
		fm.write_results(results)
		print(f'\nTop Arb: {results[0]}')
	else:
		print('\nNo Arbs')
