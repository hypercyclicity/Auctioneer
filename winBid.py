import urllib
import time
import threading
import sqlite3
import datetime
import re
import sys
from datetime import timedelta


def DataBuilder():
	try:
		d = timedelta(seconds=10)
		f = open('../winBidx.csv','w')
		y = open('../winBidy.csv','w')
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT SQLITE_VERSION()')
		data = cur.fetchone()
		print "SQLite version: %s" % data
		
		cur.execute('SELECT b.price, b.time_left, b.bid_date, b.hour, b.value, b.isGameplay, b.isVoucher FROM bid b')
		allentries = cur.fetchall();
		for x in allentries:
			price = x[0]
			time_left  = x[1]
			bid_date = x[2]
			hour = x[3]
			value = x[4]
			isGameplay = x[5]
			isVoucher = x[6]
			print bid_date
			newtime = bid_date
			newtime.seconds = newtime.seconds - 10
			print newtime
			sys.exit(0)
		f.close()
		y.close()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	DataBuilder()
	
