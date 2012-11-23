import subprocess
import watch
import 
# import server
# s = server.Server()
# s.launchProgram(prog = "name of program",args=[cmd line args],file_name = "to be redirected to")

class Server:

	def __init__(self,user = "sar7"):
		self.hosts = []
		for i in range(1,23):
			if i<10:
				self.hosts.append(user+"@uf0"+str(i)+".cs.ualberta.ca")
			else:
				self.hosts.append(user+"@uf"+str(i)+".cs.ualberta.ca")
		self.counter = 0
		self.max =22


	def launchProgram(self,prog = "client.py",args=[],file_name = "test1.txt"):
		prog = prog+" " +args
		subprocess.call(["ssh",self.hosts[self.counter], "python ~/466/project/Auctioneer/"+ prog +" > ~/466/project/data/" + file_name]);
		self.counter = (self.counter +1)% self.max

if __name__ == "__main__":
        s = Server()

        siteContent = watch.getSiteContent(1)
        auctionList = watch.getCurrentAuctions(siteContent)
        auctionInfo = watch.compileCurrentAuctions(auctionList, siteContent)

        arg = ""
        for a in auctionInfo:
                arg = arg + str(a['id']) + ' "' + str(a['name']) + '" '
		
	f = str(time.time())+".txt"
        s.launchProgram(args=arg,file_name=f)
