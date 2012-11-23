import subprocess

# import server
# s = server.Server()
# s.launchProgram(prog = "name of program",args=[cmd line args],file_name = "to be redirected to")

class Server:

	def __init__(self):
		self.hosts = []
		for i in range(1,23):
			if i<10:
				self.hosts.append("sar7@uf0"+str(i)+".cs.ualberta.ca")
			else:
				self.hosts.append("sar7@uf"+str(i)+".cs.ualberta.ca")
		self.counter = 0
		self.max =22


	def launchProgram(self,prog = "hello.py",args=[],file_name = "test1.txt"):
		for arg in args:
			arg_string = arg_string  + " " + arg
		prog = prog + arg_string
		subprocess.call(["ssh",self.hosts[self.counter], "python ~/466/project/Auctioneer/"+ prog +" > ~/466/project/data/" + file_name]);
		self.counter = (self.counter +1)% self.max



