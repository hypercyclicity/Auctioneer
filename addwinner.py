import urllib
import time
import threading
import sqlite3
import datetime
import re
import sys

def DataBuilder():
	try:
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT SQLITE_VERSION()')
		data = cur.fetchone()
		print "SQLite version: %s" % data
		
		cur.execute('SELECT Distinct b.id FROM bid b')
		allentries = cur.fetchall();
		for x in allentries:
			id = x
			maxPrice = 0.0;
		 	winID = "";
			query = ("SELECT b.id, b.price FROM bid b WHERE b.id = ? ")
			cur.execute(query,id)
			isFirst = 1
			size = 0;
			for row in cur:
				for z in row:
					if isFirst == 1:
						id = z
						isFirst = 0;					
					else:
						price = z
				if price > maxPrice:
					maxPrice = price
					winId = id
				size = size + 1
			try:
				cur.execute("INSERT INTO winner(id,price,numBids) VALUES(?,?,?)",(winId,maxPrice,size))
			except sqlite3.Error, e:
				print "Error Insert %s:" % e.args[0]
				sys.exit(1)	
		con.close()
	except sqlite3.Error, e:
		print "Error Select %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	DataBuilder()
	
