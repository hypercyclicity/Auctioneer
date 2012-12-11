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
import Util



def DataBuilder():
	try:
		sep = " "
		secs10 = timedelta(seconds=10)
		d = timedelta(seconds=10)
		f = open('./data/winBidx.csv','w')
		f.write("prince,time_left,time,dif_time,count10secs,count1min,count5min,hour,value,gameplay,isVoucher,y\n")
		y = open('./data/winBidy.csv','w')
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
			winning = Util.IsWinningBid(thisID, price, cur)
			if( c < 1100 or winning == 1):
				less10secs = bid_date - timedelta(seconds=10)
				less1min   = bid_date - timedelta(seconds=60)
				less5min   = bid_date - timedelta(minutes = 5)
			
				count10secs = Util.GetNumAftertime(less10secs,thisID,cur)
				count1min = Util.GetNumAftertime(less1min,thisID,cur)
				count5min =  Util.GetNumAftertime(less5min,thisID,cur)
				time = calendar.timegm(bid_date.timetuple())
				timeSinceLast = Util.GetTimeSinceLastBid(price, thisID, time, cur)

				f.write(str(price) + sep )
				f.write(str(time_left) +sep )
				f.write(str(time) + sep)
				f.write(str(timeSinceLast) + sep)
				f.write(str(count10secs) + sep)
				f.write(str(count1min) + sep)
				f.write(str(count5min) + sep)
				f.write(str(hour) + sep)
				f.write(str(value) + sep )
				f.write(str(isGameplay) + sep )
				f.write(str(isVoucher) + "\n")
				winning = Util.IsWinningBid(thisID, price, cur)
				y.write(str(winning) + "\n" )
				print c," bids complete complete         \r",
				c = c+1
			if c == 2000:
				break
		f.close()
		y.close()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	DataBuilder()
	
