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
'''
def GetTimeForlastSoManyBids(price,thisID,cur):
	query = 'SELECT b.bid_date FROM bid b WHERE b.price == ? AND b.id == ?'
	cur.execute(query, (price,thisID))
	temp =  cur.fetchall();
	print len(temp)
	#sys.exit(1)
'''

def StringToUTC(date_Str):
	try:
		bid_date = datetime.strptime(date_Str, "%Y-%m-%d %H:%M:%S.%f")
	except ValueError:
		bid_date = datetime.strptime(date_Str, "%Y-%m-%d %H:%M:%S")
	return bid_date
			
def GetMindate(thisID,user,cur):
	cur.execute('SELECT min(b.bid_date) FROM bid b WHERE b.user == ? AND b.id == ? ' , 			(user,thisID))
	date = cur.fetchall()[0][0]
	return StringToUTC(date)
	
def GetMaxdate(thisID,user,cur):
	cur.execute('SELECT max(b.bid_date) FROM bid b WHERE b.user == ? AND b.id == ? ' , 			(user,thisID))
	date = cur.fetchall()[0][0]
	return StringToUTC(date)
	
def IsWinningBid(thisID, price, cur):
	cur.execute('SELECT count(w.price) FROM winner w WHERE w.id == ? AND w.price ==?',(thisID,price))
	x = cur.fetchall();
	return x[0][0]

def GetNumAftertime(time ,thisID, cur):
	query = 'Select count(*) FROM bid b where b.bid_date > ? and b.id == ?' 
	cur.execute(query, (time,thisID));
	temp =  cur.fetchall();
	return temp[0][0]

def GetTimeSinceLastBid(price, thisID, time, cur):
	query = 'SELECT b.bid_date,max(b.price) FROM bid b Where b.id == ? AND b.price < ?' 
	cur.execute(query, (thisID,price));
	temp = cur.fetchall()[0][0];
	if temp == None:
		return 0
	preTime = calendar.timegm(StringToUTC(temp).timetuple())
	return time - preTime
