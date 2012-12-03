import urllib
import time
import threading
import sqlite3
import datetime
import re
import sys
from datetime import timedelta
from datetime import datetime

def GetNumAftertime(time ,thisID, cur):
	query = 'Select count(*) FROM bid b where b.bid_date > ? and b.id == ?' 
	cur.execute(query, (time,thisID));
	temp =  cur.fetchall();
	return temp[0][0]

#def GetTimeForlastSoManyBids(numBids,thisID,cur)
#	query = 'SELECT 

def DataBuilder():
	try:
		secs10 = timedelta(seconds=10)
		d = timedelta(seconds=10)
		f = open('../data/winBidx.csv','w')
		y = open('../data/winBidy.csv','w')
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT SQLITE_VERSION()')
		data = cur.fetchone()
		print "SQLite version: %s" % data
		
		cur.execute('SELECT b.price, b.time_left, b.bid_date, b.hour, b.value, b.isGameplay, b.isVoucher, b.id FROM bid b')
		allentries = cur.fetchall();
		for x in allentries:
			price = x[0]
			time_left  = x[1]
			bid_date_str = x[2]
			try:
				bid_date = datetime.strptime(bid_date_str, "%Y-%m-%d %H:%M:%S.%f")
			except ValueError:
				bid_date = datetime.strptime(bid_date_str, "%Y-%m-%d %H:%M:%S")
			hour = x[3]
			value = x[4]
			isGameplay = x[5]
			isVoucher = x[6]
			thisID = x[7]
			less10secs = bid_date - timedelta(seconds=10)
			less1min   = bid_date - timedelta(seconds=60)
			less5min   = bid_date - timedelta(minutes = 5)
			count10secs = GetNumAftertime(less10secs,thisID,cur)
			count1min = GetNumAftertime(less1min,thisID,cur)
			count5min =  GetNumAftertime(less5min,thisID,cur)
			f.write(str(price) + " " )
			sys.exit(1)
		f.close()
		y.close()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	DataBuilder()
	
