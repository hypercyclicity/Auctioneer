import subprocess
import watch
import time
import os
from operator import itemgetter
# import server
# s = server.Server()
# s.launchProgram(prog = "name of program",args=[cmd line args],file_name = "to be redirected to")

class Server:

	def __init__(self):
		self.hosts = []
		for i in range(1,23):
			if i<10:
				self.hosts.append(os.getenv('USER')+"@uf0"+str(i)+".cs.ualberta.ca")
			else:
				self.hosts.append(os.getenv('USER')+"@uf"+str(i)+".cs.ualberta.ca")
		self.counter = 0
		self.max =22


	def launchProgram(self,prog = "client.py",args=[],file_name = "test1.txt"):
		prog = prog+" " +args
		subprocess.call(["ssh",self.hosts[self.counter], "python /home/dsk03/ugrad/sar7/466/project/Auctioneer/"+ prog +" > /home/dsk03/ugrad/sar7/466/project/data/"+ file_name])
		self.counter = (self.counter +1)% self.max

	def kill_all(self):
		for x in range(1,22):
			rtn = subprocess.call(["ssh",self.hosts[self.counter],"pkill","python"])
			print ["ssh",self.hosts[self.counter],"pkill","python"]
			print rtn
			self.counter = (self.counter +1)% self.max
	
if __name__ == "__main__":
        s = Server()
	s.kill_all()
        pageNum = 4
        auctionInterval = 60*5
        oldAuctionList = []

        while True:
                siteContent = watch.getSiteContent(pageNum)
                auctionList = watch.getCurrentAuctions(siteContent)
                
                # Make sure we didn't see the auction last time
                auctionList = [x for x in auctionList if x not in oldAuctionList ]
                oldAuctionList = auctionList

                auctionInfo = watch.compileCurrentAuctions(auctionList, siteContent)

                arg = ""
                for a in auctionInfo:
                        arg = arg + str(a['id']) + ' \'' + str(a['name']) + '\' '
                        
                f = str(time.time())+".txt"
                print "Auction Request - Starting New Process"
                print "Number of auctions : " + str(len(auctionInfo))
                print arg
                print "###################"
                s.launchProgram(args=arg,file_name=f)

                time.sleep(auctionInterval)
                
