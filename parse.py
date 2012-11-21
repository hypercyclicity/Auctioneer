import urllib
import time
import threading
import sqlite3
import datetime
from BeautifulSoup import BeautifulSoup
import re


def parse():
	x=1
	while True:
		site = urllib.urlopen("http://quibidsinsider.com/auction/?page="+str(x))
		t = str(time.time())
		x = x+1
		soup = BeautifulSoup(site)
		auctions = soup.findAll('div',attrs={"class":re.compile('row odd auction.*')})
		for auction in auctions:
			try:
				title = auction.find('div',attrs={"class":"title"}).find('a').contents[0]
				bid_id =  str(auction.find('div',attrs={"class":"title"}).find('a')).split('/')[2]
				price = auction.find('div',attrs={"class":"price"}).contents[0]
				winner = auction.find('div',attrs={"class":"winner"}).find('a').contents[0]
				timeLeft = auction.find('div',attrs={"class":"timeleft"}).contents[0]
				print(bid_id + '|$|'+title + "|$|" + price + "|$|" + winner + "|$|" + timeLeft + "|$|" + t)
			except AttributeError: 
				return

if __name__ == "__main__":
	while True:
		thread = threading.Thread(target = parse)
		thread.start()
		time.sleep(1)

	



