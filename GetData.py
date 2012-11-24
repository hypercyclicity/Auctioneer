import urllib
import time
import threading
import sqlite3
import datetime
import re
import sys

def DataBuilder():
	try:
		f = open('data.csv','w')
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT SQLITE_VERSION()')
		data = cur.fetchone()
		print "SQLite version: %s" % data
		
		#cur.execute('SELECT Distinct  b.name FROM bid b WHERE b.bid_date > 2013-11-30 and
				# value <> -1')
		cur.execute('SELECT Distinct b.id FROM bid b')
		allentries = cur.fetchall();
		c = 0
		for x in allentries:
			id = x
			query = ("SELECT min(b.hour), max(b.hour), max(b.price), count(*)  						FROM bid b WHERE b.id = ? ")
			cur.execute(query,id)
			isFirst = 1
			for row in cur:
				for z in row:
					if isFirst == 1:
						isFirst = 0
					else:
						f.write(" ")
					f.write(str(z))
			f.write("\n")
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	DataBuilder()
	
