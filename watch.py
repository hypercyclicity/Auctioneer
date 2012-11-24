import urllib
import time
import threading
import sqlite3
import datetime
import re
import base64
import sys
import json
from operator import itemgetter

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

    site = urllib.urlopen("http://quibidsinsider.com/ajax/", request)

    content = site.read()
    site.close()
    return content

def getCurrentAuctions(siteContent):
    """
    http://stackoverflow.com/a/1732454
    """
    oddAuctions = [m.start() for m in re.finditer('row odd auction-', siteContent)]
    evenAuctions = [m.start() for m in re.finditer('row even auction-', siteContent)]
    auctions = [siteContent[i+16:i+32] for i in oddAuctions] + [siteContent[i+17:i+33] for i in evenAuctions]
    return auctions

def getSiteContent(page):
    site = urllib.urlopen("http://quibidsinsider.com/auction/?page=" + str(page))
    siteContent = site.read()
    site.close()
    return siteContent

def compileCurrentAuctions(auctions, siteContent):
    auctionInfo = []
    auctionDict = {}

    i = 0
    for a in auctions:
        auctionDict = {}
        auctionDict['id'] = a
        reTitle = re.compile('/auction/' + auctions[i] + '/"(?:(?!</a>).)*')
        auctionDict['name'] = reTitle.search(siteContent).group(0)[28:]
        auctionInfo.append(auctionDict)
        i = i + 1

    return auctionInfo

def prettyPrint(auctionInfo):
    oldAuctionsZero = []
    oldOldAuctionsZero = []
    oldOldOldAuctionsZero = []
    while True:
        time.sleep(1)
    
        # You can actually send all the ids at once
        idString = ''.join(n['id'] for n in auctionInfo)
    
        info = getAuctionInfo(idString)
        data = json.loads(info)

        lastAuctionUpdate = data['lts']
       # sys.stderr.write("Last Auction Update : " + str(lastAuctionUpdate) + "\n")
        #sys.stderr.write("Number of auctions being watched : " + str(len(auctionInfo)) + "\n")

        auctionsZero = []
        
        for i in range(len(data["a"])):
            # Grab the dictionary for a specific auction, append the auction number
            auctionJSON = data["a"][i][data["a"][i].keys()[0]]
            auctionJSON['auctionID'] = data["a"][i].keys()[0]

            try:
                print auctionInfo[map(itemgetter('id'), auctionInfo).index(str(data["a"][i].keys()[0]).upper())]['name'] + \
                    "|$|" + str(auctionJSON['auctionID']) + \
                    "|$|" + str(auctionJSON['p']) + \
                    "|$|" + str(auctionJSON['w']) + \
                    "|$|" + str(auctionJSON['tl']) + \
                    "|$|" + str(lastAuctionUpdate)

                if auctionJSON['tl'] == 0:
                        auctionsZero.append(auctionJSON['auctionID'])
            except KeyError:
                print auctionInfo[map(itemgetter('id'), auctionInfo).index(str(data["a"][i].keys()[0]).upper())]['name'] + \
                    "|$|" + str(auctionJSON['auctionID']) + \
                    "|$|" + str(auctionJSON['p']) + \
                    "|$|" + str(auctionJSON['w']) + \
                    "|$|" + "0" \
                    "|$|" + str(auctionJSON['e'])
                # Auction must be over, remove it from the list
		old_auction=str(data["a"][i].keys()[0]).upper()
                auctionInfo[:] = [d for d in auctionInfo if d.get('id') != old_auction]

        if not auctionInfo:
            # All of the auctions we are monitoring have completed
            break

        for aucID in auctionsZero:
            if aucID in oldOldOldAuctionsZero:
                auctionInfo[:] = [d for d in auctionInfo if d.get('id') != str(aucID).upper()]

        print "Length of auction info : " + str(len(auctionInfo))
        oldOldOldAuctionsZero = oldOldAuctionsZero
        oldOldAuctionsZero = oldAuctionsZero
        oldAuctionsZero = auctionsZero

if __name__ == "__main__":
    siteContent = getSiteContent(4)
    auctionList = getCurrentAuctions(siteContent)
    auctionInfo = compileCurrentAuctions(auctionList, siteContent)
    prettyPrint(auctionInfo)
