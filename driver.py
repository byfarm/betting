import file_man as fm
import ods_calc as oc
import scraping as sc


max_stake = 100
# initialize urls
dk_url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'
uni_url = 'https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687557915663&useCombined=true&useCombinedLive=true'

# scrape the websites
dk, games_d = sc.scrape_dk_mlb(dk_url)
uni, games_u = sc.scrape_unibet_mlb(uni_url)

# make sure each game is in both books
if games_u != games_d:
	for i in games_d:
		if i not in games_u:
			games_d.remove(i)
	for i in games_u:
		if i not in games_d:
			games_u.remove(i)

# write the odds and games to the txt file
fm.write_new_table_dk_uni(dk, uni, games_u)

# read the odds and games from the txt file and arrange them
odds, games = fm.read_from_file()
p = oc.arrange_odds(odds, games)
oc.arr_od_to_prob(p)

# find arbitrage opportunities
arbs = oc.find_arb(p)

if len(arbs) > 0:
	for games in arbs:
		teams_ods = games[1]
		g1 = teams_ods[:len(teams_ods)//2]
		g2 = teams_ods[len(teams_ods)//2:]
		p1 = oc.odd_to_prob(g1[0])
		p2 = oc.odd_to_prob(g2[0])
		s1, s2 = oc.det_max_in(max_stake, p1, p2)
		g1.append(s1)
		g2.append(s2)
		games[1] = g1 + g2


