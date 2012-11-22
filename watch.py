import urllib
import time
import threading
import sqlite3
import datetime
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
	"""
	http://stackoverflow.com/a/1732454
	"""
	site = urllib.urlopen("http://quibidsinsider.com/auction/?page=1")
	siteContent = site.read()
	site.close()
	oddAuctions = [m.start() for m in re.finditer('row odd auction-', siteContent)]
	evenAuctions = [m.start() for m in re.finditer('row even auction-', siteContent)]
	auctions = [siteContent[i+16:i+32] for i in oddAuctions] + [siteContent[i+17:i+33] for i in evenAuctions]
	print auctions

	# You can actually send all the ids at once
	id = ''.join(n for n in auctions)
	print getAuctionInfo(id)
	return

if __name__ == "__main__":
	getCurrentAuctions()
