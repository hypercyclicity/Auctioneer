import sqlite3
import datetime
#!/usr/bin/python
import re
import sqlite3
import csv
import time
import sys
import glob
import os
from optparse import OptionParser
            
def adder(fileName):
	duplicates = 0
	print fileName
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
				id = tokens[1]
				name = tokens[0]
				value = -1
				gamePlay = 0
				isVoucher = 0
				if name[0] == '$':
					names = name.split(" ")

					value_RHS = names[0]
					value =int(value_RHS[1:])
					
				if  "1X Gameplay" in name:
					gamePlay = 1	
				if  "Voucher Bids" in name:
					isVoucher = 1
					names = name.split(" ")
					value = names[0]
				price_string = tokens[2]
				price = float(price_string[1:])
				user = tokens[3]
				time_left = int(tokens[4])
				time_stamp = datetime.datetime.utcfromtimestamp(float(tokens[5]))
				if value != -1 and len(user) > 0 and price > 0.0:
					try:
						cur.execute("INSERT INTO bid(id,name,price,user,time_left,bid_date, hour,value,isGameplay,isVoucher) VALUES(?,?,?,?,?,?,?,?,?,?)",(id,name,price,user,time_left,time_stamp, time_stamp.hour, value,gamePlay,isVoucher))
					except sqlite3.Error, e:
						duplicates = duplicates + 1

		f.close()
		con.commit()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	for files in glob.glob("*.txt"):
    		print files 
    		adder(files)	



