import sqlite3
import datetime
#!/usr/bin/python
import re
import sqlite3
import csv
import time
import sys
from optparse import OptionParser
            
def adder(fileName):
	duplicates = 0
	try:
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT SQLITE_VERSION()')
		data = cur.fetchone()
		print "SQLite version: %s" % data
		f = open(fileName)
		for line in f:
			tokens = line.split("|$|")
			if len(tokens) == 6:
				id = tokens[0]
				name = tokens[1]
				value = -1
				gamePlay = 0
				if name[0] == '$':
					names = name.split(" ")
					value_RHS = names[0]
					value =int(value_RHS[1:])
					
				if  "1X Gameplay" in name:
					gamePlay = 1	
				price_string = tokens[2]
				price = float(price_string[1:])
				user = tokens[3]
				time_left = int(tokens[4])
				time_stamp = datetime.datetime.utcfromtimestamp(float(tokens[5]))
				try:
					cur.execute("INSERT INTO bid(id,name,price,user,time_left,bid_date, hour,value,isGameplay) VALUES(?,?,?,?,?,?,?)",(id,name,price,user,time_left,time_stamp, time_stamp.hour, value,gamePlay))
				except sqlite3.Error, e:
					duplicates = duplicates + 1

		f.close()
		con.commit()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":

	for each in sys.argv[1:]:
		adder(each)


