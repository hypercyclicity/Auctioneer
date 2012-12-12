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

"""
A .csv file is created for X and Y matrices to determine whether the
next bid will be the final bid in an auction.

X = A matrix of rows of 9 bids

Y = A classification matrix of whether the next (10th in the sequence) bid wins (1 == yes)

"""
def GetWinningPrice(thisID,cur):
	cur.execute('SELECT w.price FROM winner w WHERE w.id == ?',(thisID))
	x = cur.fetchall()[0][0]
	return x
	
def DataBuilder():
	breakNum = 2000
	try:
		sep = ","
		xMatrix = open('./data/priceX.csv','w')
		xMatrix.write("a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,aa,ab,ac,ad,af,a1,a2,a3,a4,a5,a6,a7,a8,a9,a0,q1,w2,e3,r4,t5,y6,u7,i8,o9,p0")
		xMatrix.write(",s1,d2,f3,g4,h5,j6,k7,l8,l9,l0,l6,l5,l4,l3,l2,l1,z1,z2,z3,z4,z5,z6,z7,z8,z9,z0,x1x,x2,x3,x4,x5,x6,x7,x8,x9,x0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m0,m12,m11\n")
		yMatrix = open('./data/priceY.csv','w')
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT DISTINCT id FROM bid;')
		auctions = cur.fetchall()
		c = 0
		step = 0
		for auction in auctions:
			if c >= breakNum:
				break
                        query = 'SELECT * FROM bid WHERE id == ? ORDER by price;'
                        cur.execute(query, auction)
                        bids = cur.fetchall()
                        # We need at least 10 bids to do this
                        if len(bids) > 9:
                                for i in range(0,len(bids) - 10 + 1):
                                	step = step + 1
                                	if c >= breakNum:
						break
                                        # Leaving users out at the moment
                                        bidslice = bids[i:i+9]  # first nine
                                        last = bids[i+9]        # number ten
                                        
                                        # Query if last is the winner
					query = 'SELECT count(*) FROM winner WHERE id == ? AND price == ?;'
					
                                        cur.execute(query, (last[0], last[2]))
                                        isWinner = cur.fetchone()[0]
                                        if( step%5 == 0 ):
		                                
		                                result = GetWinningPrice(auction,cur)
		                                
		                                spaceCounter = 0
		                                for b in bidslice:
		                                	spaceCounter = spaceCounter + 1
		                                        price = b[2]
		                                        timeLeft = b[4]
		                                        bidDate = Util.StringToUTC(str(b[5]))
		                                        less10secs = bidDate - timedelta(seconds=10)
							less1min   = bidDate - timedelta(seconds=60)
							less5min   = bidDate - timedelta(minutes = 5)
		                                        hour = b[6]
		                                        value = b[7]
		                                        isGameplay = b[8]
		                                        isVoucher = b[9]
							count10secs = Util.GetNumAftertime(less10secs,b[0],cur)
							count1min = Util.GetNumAftertime(less1min,b[0],cur)
							count5min =  Util.GetNumAftertime(less5min,b[0],cur)
							time = calendar.timegm(bidDate.timetuple())
							timeSinceLast = Util.GetTimeSinceLastBid(price, b[0], time, cur)
							xMatrix.write(str(timeSinceLast) + sep)
							xMatrix.write(str(count10secs) + sep)
							xMatrix.write(str(count1min) + sep)
							xMatrix.write(str(count5min) + sep)
		                                        xMatrix.write(str(price) + sep )
		                                        xMatrix.write(str(timeLeft) + sep )
		                                        xMatrix.write(str(time) + sep)	
		                                        xMatrix.write(str(hour) + sep )
		                                        xMatrix.write(str(value) + sep )
		                                        xMatrix.write(str(isGameplay) + sep )
		                                        xMatrix.write(str(isVoucher))
		                                        if spaceCounter < 9:
		                                        	xMatrix.write(",")
		                                # Close the row
		                               # xMatrix.write("\n")
		                                xMatrix.write(str(result) + "\n")
                                                c = c +1
                                                print c
                                        	if c >= breakNum:
							break

                                     	
                
                # End auction loop
		xMatrix.close()
		yMatrix.close()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	DataBuilder()
