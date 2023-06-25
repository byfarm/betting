import plus_ev

if __name__ == '__main__':
	import file_man as fm
	import ods_calc as oc
	import scraping as sc
	import betting_calcs as bc
	import main_functions as mf
	import plus_ev as pe

	max_stake = 100
	#mf.scrape_web()

	odds = mf.assemble_from_file()

	evs = mf.find_plus_ev(odds)
	sort_evs = pe.insert_sort_h_to_l(evs)
	# find arbitrage opportunities
	arbs = mf.find_arb(odds)

	if len(arbs) > 0:
		results = bc.add_stake(arbs, max_stake)
		fm.write_results(results)
		print('New Results in!')
	else:
		print('No opportunities')
