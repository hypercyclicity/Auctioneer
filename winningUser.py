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
		secs10 = timedelta(seconds=10)
		d = timedelta(seconds=10)
		f = open('./data/winningUserX.csv','w')
		y = open('./data/winningUserY.csv','w')
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT SQLITE_VERSION()')
		data = cur.fetchone()
		print "SQLite version: %s" % data
		
		cur.execute('SELECT distinct  b.id FROM bid b')
		allentries = cur.fetchall();
		c = 0
		step = 0
		for x in allentries:
			ID = x[0]
			cur.execute('SELECT count(*), min(b.value), min(b.hour), min(b.isGameplay), min(b.isVoucher) FROM bid b WHERE b.id ==?',(ID,));
			thisAuction = cur.fetchall()
			totalbids = thisAuction[0][0];
			value = thisAuction[0][1]
			hour = thisAuction[0][2]
			isGameplay = thisAuction[0][3]
			isVoucher = thisAuction[0][4]
			cur.execute('SELECT distinct b.user FROM bid b WHERE b.id == ?',(ID,))
			allusers = cur.fetchall();
			for use in allusers:
				step = step + 1
				winning = Util.IsWinningUser(ID, use[0], cur)
				if ((step%8 == 0 and c < 2000) or (step%5 == 0 and winning == 1 )):
					cur.execute('SELECT count(*) FROM bid b WHERE b.id == ? AND 					user == ?', (ID,use[0]))
					totalUserBids = cur.fetchall()[0][0];
					minbiddate = calendar.timegm(Util.GetMindate(ID,use[0], cur).timetuple())
					maxbiddate = calendar.timegm(Util.GetMaxdate(ID,use[0], cur).timetuple())
					if totalUserBids != 1:
						aveTimeBetweenBids = (maxbiddate - minbiddate)/(totalUserBids-1)
					else:
						aveTimeBetweenBids =0				
				
					f.write(str(totalbids) + " " )
					f.write(str(value) + " " )
					f.write(str(hour) + " ")	
					f.write(str(hour) + " " )
					f.write(str(value) + " " )
					f.write(str(isGameplay) + " " )
					f.write(str(isVoucher) + " " )
					f.write(str(totalUserBids) + " " )
					f.write(str(minbiddate) + " " )
					f.write(str(maxbiddate) + " " )
					f.write(str(aveTimeBetweenBids) + "\n" )
					y.write(str(winning) + "\n")
					print c," bids complete complete         \r",
					c = c+1
					if c >= 2000:
						break
			if c >= 2000:
				break
		f.close()
		y.close()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
    		
if __name__ == "__main__":
	DataBuilder()
	
