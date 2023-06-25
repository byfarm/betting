if __name__ == '__main__':
	import file_man as fm
	import ods_calc as oc
	import scraping as sc
	import betting_calcs as bc
	import main_functions as mf

	max_stake = 100
	mf.scrape_web()

	odds, games = mf.assemble_from_file()

	# find arbitrage opportunities
	arbs = mf.find_arb(odds)

	if len(arbs) > 0:
		results = bc.add_stake(arbs, max_stake)
		fm.write_results(results)
		print('New Results in!')
	else:
		print('No opportunities')
