import file_man as ctf
import scraping as sc
import pytest
import ods_calc as oc
import copy


def test_website_access():
	# paste desired url
	url = 'https://www.pinnacle.com/en/baseball/mlb/matchups/#period:0'
	status_code = sc.allow_access(url)
	assert status_code == 200

def test_file_open():
	dk_url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'
	uni_url = 'https://eu-offering-api.kambicdn.com/offering/v2018/ubusva/listView/baseball/mlb/all/all/matches.json?lang=en_US&market=US-VA&client_id=2&channel_id=1&ncid=1687557915663&useCombined=true&useCombinedLive=true'
	dk, games_d = sc.scrape_dk_mlb(dk_url)
	uni, games_u = sc.scrape_unibet_mlb(uni_url)

	for i in games_d:
		if i not in games_u:
			games_d.remove(i)

	ctf.write_new_table_dk_uni(dk, uni, games_u)
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


def test_read_from_file():
	r = ctf.read_from_file()
	print(r)
	assert len(r) == 2


def test_ods_to_percent():
	prob = oc.odd_to_prob(-400)
	assert prob == 0.8


def test_arr_odes():
	odds, games = ctf.read_from_file()
	p = oc.arrange_odds(odds, games)
	assert len(p.values()) == 11


def test_odds_to_arr_prob():
	odds, games = ctf.read_from_file()
	p = oc.arrange_odds(odds, games)
	oc.arr_od_to_prob(p)
	print(p)


