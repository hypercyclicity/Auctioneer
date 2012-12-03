import urllib
import time
import threading
import sqlite3
import datetime
import re
import sys
from datetime import timedelta
from datetime import datetime
import calendar

def IsWinningBid(thisID, price, cur):
	cur.execute('SELECT count(w.price) FROM winner w WHERE w.id == ? AND w.price ==?',(thisID,price))
	x = cur.fetchall();
	return x[0][0]

def GetNumAftertime(time ,thisID, cur):
	query = 'Select count(*) FROM bid b where b.bid_date > ? and b.id == ?' 
	cur.execute(query, (time,thisID));
	temp =  cur.fetchall();
	return temp[0][0]

def GetTimeForlastSoManyBids(price,thisID,cur):
	query = 'SELECT b.bid_date FROM bid b WHERE b.price == ? AND b.id == ?'
	cur.execute(query, (price,thisID))
	temp =  cur.fetchall();
	print len(temp)
	#sys.exit(1)

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
		c = 0
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
			
			timeLast10Bids = 0
			timeLast20Bids = 0
			if price > 0.10:
				timeLast10Bids = GetTimeForlastSoManyBids(price-.1,thisID,cur)
			f.write(str(price) + " " )
			f.write(str(time_left) + " " )
			f.write(str(calendar.timegm(bid_date.timetuple())) + " ")	
			f.write(str(hour) + " " )
			f.write(str(value) + " " )
			f.write(str(isGameplay) + " " )
			f.write(str(isVoucher) + "\n" )
			y.write(str(IsWinningBid(thisID, price, cur)) + "\n")
		#	print c," bids complete complete         \r",
			c = c+1
		f.close()
		y.close()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	DataBuilder()
	
