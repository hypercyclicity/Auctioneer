import urllib
import time
import threading
import sqlite3
import datetime
import re
import sys

def addRatio():
	try:
		f = open('datax.csv','w')
		y = open('datay.csv','w')
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT SQLITE_VERSION()')
		data = cur.fetchone()
		print "SQLite version: %s" % data
		
		cur.execute('SELECT Distinct b.user FROM bid b')
		
		allentries = cur.fetchall()
		c = 0
		for x in allentries:
			user = x

			query = ("SELECT count(*) FROM bid WHERE user == ?")
			cur.execute(query,user)

                        numBids = cur.fetchone()[0]

                        query = ("SELECT count(*) FROM winner WHERE user == ?")
                        cur.execute(query,user)

                        numWins = cur.fetchone()[0]

                        print user[0]
                        print numBids
                        print numWins

                        ratio = numWins / numBids

                        try:
				cur.execute("INSERT INTO ratio(user, totalWins, numBids) VALUES(?,?,?)",(user[0],numWins,numBids))
			except sqlite3.Error, e:
				print "Error Insert %s:" % e.args[0]
				sys.exit(1)

                f.close()
		con.commit()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
        addRatio()
	
