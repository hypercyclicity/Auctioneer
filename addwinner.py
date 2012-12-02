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
		 	winUser = ""
			query = ("SELECT b.id, b.price, b.user FROM bid b WHERE b.id == ? ")
			cur.execute(query,id)
			isFirst = 1
			size = 0;
			for row in cur:
				for z in row:
					if isFirst == 1:
						idu = z
						isFirst = 2;					
					elif isFirst == 2:
						price = z
					     	isFirst = 3;
					else:
						user = z
				if price > maxPrice:
					maxPrice = price
					winID = idu
					winUser = user
				size = size + 1
			try:
				if maxPrice > 0.0:
					cur.execute("INSERT INTO winner(id,price,numBids,user) VALUES(?,?,?,?)"
					,(winID,maxPrice,size,winUser))
			except sqlite3.Error, e:
				print "Error Insert %s:" % e.args[0]
				sys.exit(1)	
		con.commit()
		con.close()
	except sqlite3.Error, e:
		print "Error Select %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	DataBuilder()
	
