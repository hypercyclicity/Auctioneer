import sqlite3
import datetime
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
				price = float(price_string)
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
		
def addwinner():
	try:
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT SQLITE_VERSION()')
		data = cur.fetchone()
		print "SQLite version: %s" % data
		
		cur.execute('SELECT b.id, max(b.price), b.user FROM bid b Group by b.id')
		allentries = cur.fetchall();
		for x in allentries:
			winID = x[0];
			yyyy = str(winID)
			maxPrice = x[1];
			winUser = x[2];
			query = "SELECT count(*) FROM bid b Where b.id == ?"
			cur.execute(query,(winID,))
			sizes = cur.fetchall();
			size = sizes[0][0]
			try:
				if maxPrice > 0.0:
					cur.execute("INSERT INTO winner(id,price,numBids,user) VALUES(?,?,?,?)"
					,(winID,maxPrice,size,winUser))
			except sqlite3.Error, e:
				print "Error Insert %s:" % e.args[0]
		con.commit()
		con.close()
	except sqlite3.Error, e:
		print "Error Select 2 %s:" % e.args[0]
		sys.exit(1)

def RemoveBadData():
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
			query = ("SELECT count(b.id) FROM bid b WHERE b.id == ? ")
			cur.execute(query,id)
			for row in cur:
				for z in row:
					if z == 1:
						try:
							cur.execute("DELETE FROM bid  WHERE id == ?", id)
							cur.execute("DELETE FROM winner  WHERE id == ?", id)
						except sqlite3.Error, e:
							print "Error Insert2 %s:" % e.args[0]
							sys.exit(1)	
		con.close()
	except sqlite3.Error, e:
		print "Error Select %s:" % e.args[0]
		sys.exit(1)
		    		
if __name__ == "__main__":
	for files in glob.glob("*.txt"):
    		print files 
    		adder(files)
    	RemoveBadData()
    	addwinner()	



