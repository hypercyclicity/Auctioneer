import subprocess
import watch

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
#		prog = prog+args
                call1 = ["python"]
                call1.append("~/C466/Project/Auctioneer/" + prog) # +" > ~/C466/Project/Data/" + file_name
                call1.append(args)
                print call1
                subprocess.call(call1)
#		subprocess.call(["ssh",self.hosts[self.counter], "python ~/466/project/Auctioneer/"+ prog +" > ~/466/project/data/" + file_name]);
		self.counter = (self.counter +1)% self.max

if __name__ == "__main__":
        s = Server()

        siteContent = watch.getSiteContent(1)
        auctionList = watch.getCurrentAuctions(siteContent)
        auctionInfo = watch.compileCurrentAuctions(auctionList, siteContent)

        arg = ""
        for a in auctionInfo:
                arg = arg + str(a['id']) + ' "' + str(a['name']) + '" '

        s.launchProgram(args=arg)
