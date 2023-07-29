# betting

This scrapes sportsbetting webistes and pulls the best odds. It uses Pinnacle Sportsbook to look for plus EV opportunities, and looks across all sportsbooks to find arbitrage (risk free) opportunies. 
Look in the driver file to run the project. You can look in the live_odds.txt to find all the games and the live odds, arb_opps.txt to final all arbitrage opportunites, and plus_ev_opps.txt for all pluss EV opportunites.

In the future it will be able to find best odds across all sites and return the best for each game.

Pinnacle sportsbook webiste uses selenium to scrape and periodically needs to be updated as their html code changes. All the rest use reqests and beautifulsoup4. 
