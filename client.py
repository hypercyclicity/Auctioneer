import time
import os
import sys
import watch

if __name__ == "__main__":

#	try:
#        	pid = os.fork()
#        	if pid > 0:
#                	sys.exit(0)
#     	except OSError, e:
#        	sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
#        	sys.exit(1)

        auctionInfo = []
        auctionDict = {}
        i = 0
        for arg in sys.argv:


                if i == 0:
                        i = 1
                        continue

                if i == 1:
                        auctionDict['id'] = arg
                        i = 2
                        continue
                if i == 2:
                        auctionDict['name'] = arg
                        auctionInfo.append(auctionDict)
                        auctionDict = {}
                        i = 1
        
        watch.prettyPrint(auctionInfo)
