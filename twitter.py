#!/usr/bin/python

# wsd project main script

# hardware: ws2801 led strips + raspberry pi + internet adapter
# software pulls twits from an 'admin' (twits and retwits) and 
# displays the last result through the led strip 

# Written by Pratipo.org, hightly based on Adafruit's IoT Pinter. MIT license.
# MUST BE RUN AS ROOT (due to GPIO access)

import base64, HTMLParser, httplib, json, sys, urllib, zlib
from unidecode import unidecode


# Configurable globals.  Edit to your needs. -------------------------------

# Twitter application credentials -- see notes above -- DO NOT SHARE.
consumer_key    = '4pAHhcZkY3dSFGl4yse99g'
consumer_secret = 'nTBsNRjrp87r9GsVYFKdt5dvV0TjeGesGIFR0ZWXWsA'

# queryString can be any valid Twitter API search string, including
# boolean operators.  See http://dev.twitter.com/docs/using-search
# for options and syntax.  Funny characters do NOT need to be URL
# encoded here -- urllib takes care of that.
queryString = 'pratipo'

# Other globals.  You probably won't need to change these. -----------------
host      = 'api.twitter.com'
authUrl   = '/oauth2/token'
searchUrl = '/1.1/search/tweets.json?'
agent     = 'wsd app v0.1'
# lastID is command line value (if passed), else 1
if len(sys.argv) > 1: lastId = sys.argv[1]
else:                 lastId = '1'

# Initiate an HTTPS connection/request, uncompress and JSON-decode results
def issueRequestAndDecodeResponse(method, url, body, headers):
  connection = httplib.HTTPSConnection(host)
  connection.request(method, url, body, headers)
  response = connection.getresponse()
  if response.status != 200:
    # This is OK for command-line testing, otherwise 
    # keep it commented out when using main.py
    # print('HTTP error: %d' % response.status)
    exit(-1)
  compressed = response.read()
  connection.close()
  return json.loads(zlib.decompress(compressed, 16+zlib.MAX_WBITS))


# Mainline code. -----------------------------------------------------------
#print " > getting token"

# Get access token. --------------------------------------------------------
token = issueRequestAndDecodeResponse(
  'POST', authUrl, 'grant_type=client_credentials',
   {'Host'            : host,
    'User-Agent'      : agent,
    'Accept-Encoding' : 'gzip',
    'Content-Type'    : 'application/x-www-form-urlencoded;charset=UTF-8',
    'Authorization'   : 'Basic ' + base64.b64encode(urllib.quote(consumer_key) + ':' + urllib.quote(consumer_secret))}
  )['access_token']


# Perform search. ----------------------------------------------------------
#print "  > getting data"

data = issueRequestAndDecodeResponse(
  'GET',
  (searchUrl + 'count=1&q=%s' % (urllib.quote(queryString))),
  None,
  {'Host'            : host,
   'User-Agent'      : agent,
   'Accept-Encoding' : 'gzip',
   'Authorization'   : 'Bearer ' + token})


# Display results. ---------------------------------------------------------
#print "   > displaying token"

for tweet in data['statuses']:
  #print('    ' + tweet['user']['screen_name'])
  #print('    ' + tweet['created_at'])
  # Remove HTML escape sequences
  # and remap Unicode values to nearest ASCII equivalents
  print(unidecode(HTMLParser.HTMLParser().unescape(tweet['text'])))

#print(data['search_metadata']['max_id_str']) # Piped back to calling process
