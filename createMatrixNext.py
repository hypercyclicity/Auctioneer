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
	try:
		xMatrix = open('./data/predictNextBidX.csv','w')
		yMatrix = open('./data/predictNextBidY.csv','w')
		con = sqlite3.connect('auction.db')
		cur = con.cursor()
		cur.execute('SELECT DISTINCT id FROM bid;')
		auctions = cur.fetchall()
		for auction in auctions:
                        query = 'SELECT * FROM bid WHERE id == ?;'
                        cur.execute(query, auction)
                        bids = cur.fetchall()

                        print "Length of bids : ", len(bids)

                        # We need at least 10 bids to do this
                        if len(bids) > 9:
                                for i in range(0,len(bids) - 10 + 1):
                                        # Leaving users out at the moment
                                        bidslice = bids[i:i+9]  # first nine
                                        last = bids[i+9]        # number ten

                                        for b in bidslice:
                                                price = b[2]
                                                timeLeft = b[4]
                                                bidDate = Util.StringToUTC(str(b[5]))
                                                hour = b[6]
                                                value = b[7]
                                                isGameplay = b[8]
                                                isVoucher = b[9]
                                                
                                                xMatrix.write(str(price) + " " )
                                                xMatrix.write(str(timeLeft) + " " )
                                                xMatrix.write(str(calendar.timegm(bidDate.timetuple())) + " ")	
                                                xMatrix.write(str(hour) + " " )
                                                xMatrix.write(str(value) + " " )
                                                xMatrix.write(str(isGameplay) + " " )
                                                xMatrix.write(str(isVoucher) + " " )

                                        # Close the row
                                        xMatrix.write("\n")
                                                
                                        # Query if last is the winner
                                        query = 'SELECT count(*) FROM winner WHERE id == ? AND price == ?;'
                                        cur.execute(query, (last[0], last[2]))
                                        isWinner = cur.fetchone()[0]
                                        
                                        yMatrix.write(str(isWinner) + "\n")
                
                # End auction loop
		xMatrix.close()
		yMatrix.close()
		con.close()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
    		
if __name__ == "__main__":
	DataBuilder()
