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

def DataBuilder():
	breakNum = 2000
	try:
		sep = " "
		xMatrix = open('./data/predictNextBidX.csv','w')
		yMatrix = open('./data/predictNextBidY.csv','w')
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT DISTINCT id FROM bid;')
		auctions = cur.fetchall()
		c = 0
		step = 0
		for auction in auctions:
			step = step + 1
			if c >= breakNum:
				break
                        query = 'SELECT * FROM bid WHERE id == ? ORDER by price;'
                        cur.execute(query, auction)
                        bids = cur.fetchall()
                        # We need at least 10 bids to do this
                        if len(bids) > 9 and step & 1  :
                                for i in range(0,len(bids) - 10 + 1):
                                	if c >= breakNum:
						break
                                        # Leaving users out at the moment
                                        bidslice = bids[i:i+9]  # first nine
                                        last = bids[i+9]        # number ten
                                        
                                        # Query if last is the winner
					query = 'SELECT count(*) FROM winner WHERE id == ? AND price == ?;'
                                        cur.execute(query, (last[0], last[2]))
                                        isWinner = cur.fetchone()[0]
                                        step  = step +1
                                        if( (step%5 == 0 and c < 2000) or (step%3 == 0 and isWinner == 1 )):
		                                
		                                yMatrix.write(str(isWinner) + "\n")
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
		                                        xMatrix.write(str(price) + " " )
		                                        xMatrix.write(str(timeLeft) + " " )
		                                        xMatrix.write(str(time) + " ")	
		                                        xMatrix.write(str(hour) + " " )
		                                        xMatrix.write(str(value) + " " )
		                                        xMatrix.write(str(isGameplay) + " " )
		                                        xMatrix.write(str(isVoucher))
		                                        if spaceCounter < 9:
		                                        	xMatrix.write(" ")
		                                # Close the row
		                                xMatrix.write("\n")
                                                c = c +1
                                                step  = step +1
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
