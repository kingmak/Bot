#!/usr/bin/env python
# make script executable: chmod 777 name.py
# execute like this: ./name.py

'''
to get bs4 and requests

linux:
    sudo apt-get update
    sudo apt-get install python-requests
    sudo apt-get install python-bs4

windows:
    pip install --upgrade pip
    pip install requests
    pip install beautifulsoup4
'''

import sys
from time import sleep, strftime

__Authors__ = ['kingmak']

### check if bs4 and requests installed
try:
    from bs4 import BeautifulSoup
    import requests
except Exception, e:
    sys.exit('Error: %s' % e)   

### get site
def getSite(link): # should check the status code but meh
    response = requests.get(link)
    html = response.text
    return html

### TODO: self update from github
#def selfUpdate():


### get jummah time n loc from https://www.msaumn.org/
def getJummahData():
    link = 'http://www.msaumn.org'
    html = getSite(link)

    soup = BeautifulSoup(html, 'html.parser')
    spanMarker = 'docs-internal-guid-0d4666dd-00e1-c11e-645c-3a8bb04556b3'

    string = soup.findAll('span', {'id': spanMarker})[2].span.contents[0] # no regex crap to deal with
    return string

### post to groupme
def post(msg, botID):
    url = 'https://api.groupme.com/v3/bots/post?bot_id=%s&text=%s'
    requests.post(url % (botID, msg))

_day = 'Friday'
trueBot = '91ba359075a58d2fd87dcceb30'
debugBot = '8c0ef3b77fd30ac37d500c3a2a'

'''
while True:
	post('Test String', debugBot)
	sleep(5)
#sys.exit()

'''

### send alert that scripted has started
post('I am Alive', debugBot)

### Worker loop
while 1:
    day = strftime('%A')
    hour = strftime('%H')

    #print day, hour

    if day == _day and hour == '07':
        post(getJummahData(), debugBot)
        #print 'sent debug alert @ %s:%s' %(hour, strftime('%M'))

    if day == _day and hour == '08':        
        post(getJummahData(), trueBot)
        #print 'send true alert @ %s:%s' %(hour, strftime('%M'))

    # need another elif to check for update
    sleep(3600) # check once in an hour
