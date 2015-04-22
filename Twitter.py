#!/usr/bin/python

# wsd project main script

# hardware: ws2801 led strips + raspberry pi + internet adapter
# software pulls twits from an 'admin' (twits and retwits) and 
# displays the last result through the led strip 

# Written by Pratipo.org, hightly based on Adafruit's IoT Pinter. MIT license.
# MUST BE RUN AS ROOT (due to GPIO access)

import time, random, re
import base64, HTMLParser, httplib, json, sys, urllib, zlib
from unidecode import unidecode

class Twitter:
	def __init__(self):
		self.consumer_key    = '4pAHhcZkY3dSFGl4yse99g'
		self.consumer_secret = 'nTBsNRjrp87r9GsVYFKdt5dvV0TjeGesGIFR0ZWXWsA'

		self.queryString = 'from:fredforcat OR from:Lulz_Es OR from:Maria_kny OR from:Lucha_x_ti OR from:HiginiaRoig OR from:RiuYashira OR from:Nitsuga000 OR from:DMarzal OR from:kolontai1959 OR from:adestemps OR from:Mitrahus OR from:IbaiKNY OR from:alberts1986 OR from:jordisalvia OR from:Xavieret_Bonet OR from:noticiessirius OR from:xmonge OR from:aritzcirbian OR from:toret OR from:AlephPukk OR from:patxigu OR from:jordiborras OR from:okokitsme'

		self.host      = 'api.twitter.com'
		self.authUrl   = '/oauth2/token'
		self.searchUrl = '/1.1/search/tweets.json?'
		self.agent     = 'wsd app v0.1'

	def issueRequestAndDecodeResponse(self, method, url, body, headers):
		connection = httplib.HTTPSConnection(self.host)
		connection.request(method, url, body, headers)
		response = connection.getresponse()
		if response.status != 200:
			#print('HTTP error: %d' % response.status)
			exit(-1)
		compressed = response.read()
		connection.close()
		return json.loads(zlib.decompress(compressed, 16+zlib.MAX_WBITS))

	def query(self):
		token = self.issueRequestAndDecodeResponse(
			'POST', self.authUrl, 'grant_type=client_credentials',
			{'Host'           : self.host,
			'User-Agent'      : self.agent,
			'Accept-Encoding' : 'gzip',
			'Content-Type'    : 'application/x-www-form-urlencoded;charset=UTF-8',
			'Authorization'   : 'Basic ' + base64.b64encode(urllib.quote(self.consumer_key) + ':' + urllib.quote(self.consumer_secret))}
			)['access_token']

		# TODO add count!!!!
		data = self.issueRequestAndDecodeResponse(
			'GET',
			(self.searchUrl + 'count=10&q=%s' % (urllib.quote(self.queryString))),
			None,
			{'Host'           : self.host,
			'User-Agent'      : self.agent,
			'Accept-Encoding' : 'gzip',
			'Authorization'   : 'Bearer ' + token})

		return data

	def getNewest(self):
		data = self.query()
		tweet = data['statuses'][0]
		body = self.urlFreeBody(tweet)
		body.rstrip('\r\n') #.upper()
		return body

	# def xxx(self):
	# 	data = self.query()
	# 	for tweet in data['statuses']:
	# 		body = unidecode(HTMLParser.HTMLParser().unescape(tweet['text']))

	#### UTILS
	# remove urls from body
	def urlFreeBody(self, tweet):
		body = unidecode(HTMLParser.HTMLParser().unescape(tweet['text']))
		if len(tweet['entities']['urls']) > 0:
			for url in tweet['entities']['urls']:
				body = re.sub(url['url'], '', body)
		return body

