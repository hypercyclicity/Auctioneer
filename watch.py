import urllib
import time
import threading
import sqlite3
import datetime
from BeautifulSoup import BeautifulSoup
import re
import base64
import sys
import json

"""
Important Javascript:

This returns an array of numbers.
function HtB(s)
{
	var b=[];

	for(var i=0;i<s.toString().length;i+=2) {
		b[i/2]=(0x00+parseInt(s.substr(i,2),16))&(255);
	}

	return b;
}

This JavaScript function takes an array of numbers (in the range 0-255) and converts to a base64-encoded string,
then breaks long lines if necessary:
function e64(data)
{
  var str = "";
  for (var i = 0; i < data.length; i++)
    str += String.fromCharCode(data[i]);

  return btoa(str).split(/(.{75})/).join("\n").replace(/\n+/g, "\n").trim();
}
"""

def htb(data):
	"""
	Converts string of hex into list of decimals.
	"""
	i = 0
	b = []
	while i < len(data):
		b.append(0x00 + int(data[i:i+2], 16) & (255))
		i = i + 2
	print b
	return b

def encode64(data):
	"""
	Converts list of integers [0..255] to a string.
	"""
	encodedString = ""
	for num in data:
		encodedString += str(chr(num))

	encodedString = base64.b64encode(encodedString)
	return encodedString

def getAuctionInfo(auction):
	encodedString = encode64(htb(auction))
	request = "auct="+ urllib.quote(encodedString.encode("utf-8")) +"&lts=0&t=0"
	print request

	site = urllib.urlopen("http://quibidsinsider.com/ajax/", request)

	content = site.read() 
	site.close()
	return content

def getCurrentAuctions():
	site = urllib.urlopen("http://quibidsinsider.com/auction/?page=1")
	soup = BeautifulSoup(site)
	auctions = soup.findAll('div',attrs={"class":re.compile('.*auction-.*')})
	for auction in auctions:
		try:
			id = auction.find('div',attrs={"class":"title"}).findAll('a')[0]['href'].split('/')[2]
			title = auction.find('div',attrs={"class":"title"}).find('a').contents[0]
			print(id + " | " + title)
			print getAuctionInfo(id)
		except AttributeError: 
			return

if __name__ == "__main__":
	getCurrentAuctions()
"""
	auction = sys.argv[1]
	print getAuctionInfo(auction)
"""
"""
	while True:
		thread = threading.Thread(target = parse)
		thread.start()
		time.sleep(1)
"""
