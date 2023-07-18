import file_man as fm
import scraping as sc
import pytest
import ods_calc as oc
import betting_calcs as bc
import main_functions as mf
import requests


def test_website_access_comp():
	# paste desired url
	url = 'https://eu-offering-api.kambicdn.com/offering/v2018/rsi2uspa/event/live/open.json?lang=en_US&market=US-PA&client_id=2&channel_id=1&ncid=1689643196188'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
	}
	response = requests.get(url, headers=headers)
	assert response.status_code == 200



def test_web_access_simp():
	url = 'https://sports.co.foxbet.com/sportsbook/v1/api/getCompetitionEvents?competitionId=8661882&marketTypes=BBPS%2CBASEBALL%3AFTOT%3AAHCP_MAIN%2CBBML%2CBASEBALL%3AFTOT%3AML%2CBBTS%2CBASEBALL%3AFTOT%3AOU_MAIN&includeOutrights=false&skip=0&take=20&channelId=17&locale=en-us&siteId=536870914'
	response = requests.get(url)
	assert response.status_code == 200


def test_file_open():
	dk_url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'
	uni_url = 'https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687557915663&useCombined=true&useCombinedLive=true'
	dk, games_d = sc.scrape_dk_mlb(dk_url)
	uni, games_u = sc.scrape_unibet_mlb(uni_url)

	for i in games_d:
		if i not in games_u:
			games_d.remove(i)

	fm.write_new_table_dk_uni(games=games_u, DK=dk, UNI=uni)
	assert len(games_d) == len(games_u)


def test_dk_scrape():
	dk_url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'
	dk = sc.scrape_dk_mlb(dk_url)
	assert dk is not None


def test_uni_scrape():
	uni_url = 'https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687570105456&useCombined=true&useCombinedLive=true'
	uni = sc.scrape_unibet_mlb(uni_url)
	print(uni)
	assert uni is not None

def test_pin_scrape():
	r, p = sc.scrape_pin()
	assert r is not None


def test_read_from_file():
	r, p = fm.read_from_live_odds()
	print(r)
	assert len(r) == 2


def test_ods_to_percent():
	prob = oc.us_odd_to_prob(-400)
	assert prob == 0.8
	prob = oc.us_odd_to_prob(400)
	assert prob == 0.2


def test_perc_to_odds():
	odd = oc.prob_to_us_odds(0.8)
	assert odd == -400
	odd = oc.prob_to_us_odds(0.4)
	assert odd == 150


def test_int_odds_to_american():
	america = oc.dec_odds_to_us_odds(2)
	assert america == 100
	america = oc.dec_odds_to_us_odds(3)
	assert america == 200
	america = oc.dec_odds_to_us_odds(1.4)
	assert america == -250
	america = oc.dec_odds_to_us_odds(1.83)
	assert america < 0


def test_arr_odes():
	odds, games = fm.read_from_live_odds()
	p = bc.arrange_odds(odds, games)
	assert len(p.values()) == 11


def test_odds_to_arr_prob():
	odds, games = fm.read_from_live_odds()
	p = bc.arrange_odds(odds, games)
	bc.arr_od_to_prob(p)
	print(p)


def test_find_arb():
	odds, games = fm.read_from_live_odds()
	p = bc.arrange_odds(odds, games)
	bc.arr_od_to_prob(p)
	arbs = mf.find_arb(p)
	print(arbs)
	assert len(arbs) == 0


def test_max_bet():
	odds, games = fm.read_from_live_odds()
	p = bc.arrange_odds(odds, games)
	bc.arr_od_to_prob(p)
	arbs = mf.find_arb(p)
	res = bc.add_stake(arbs, 100)
	assert len(res) == len(arbs)


def test_write_results():
	odds, games = fm.read_from_live_odds()
	p = bc.arrange_odds(odds, games)
	bc.arr_od_to_prob(p)
	arbs = mf.find_arb(p)
	res = bc.add_stake(arbs, 100)
	fm.write_results(res)


def test_scrape_pin():
	pb, games_pb = sc.scrape_pointsbet()
	bet_list, games_p = sc.scrape_pin(games_pb)
	assert len(games_p) == len(bet_list) // 2


def test_scrape_betfair():
	sc.scrape_betfair()


def test_sc():
	mf.scrape_web()


def test_scrape_PB_():
	odds, games = sc.scrape_pointsbet()


def test_scrap_CSB():
	sc.scrape_CSP()


def test_scrape_FD():
	sc.scrape_FD_()


def test_scrape_FOX():
	p, l = sc.scrape_unibet_mlb()
	sc.scrape_FOX(l)


def test_scrape_BRV():
	p, l = sc.scrape_betrivers()

