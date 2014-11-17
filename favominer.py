#!/usr/bin/python

from twython import Twython # pip install twython
import time # standard lib
import pprint
import codecs
import math

# Go to https://apps.twitter.com/ to register your app to get your api keys 
CONSUMER_KEY = 'enter your key'
CONSUMER_SECRET = 'enter your secret'
ACCESS_KEY = 'enter your access key'
ACCESS_SECRET = 'enter your access secret'

twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

print "\n"
print "|------------------------------------------------------------|"
print "|  Fave-o-miner                                              |"
print "|  by webyeti                                                |" 
print "|                                                            |"
print "| A twitter favorite mining tool by webyeti. Use it on       |"
print "| yourself for archiving or on any screenname for lolz       |"
print "|                                                            |"
print "| Greetz:                                                    |"
print "| @christruncer                                              |"  
print "|                                                            |"
print "|------------------------------------------------------------|"
print "\n"

# get a screen name to mine from the user and how many faves they want to mine
user = str(raw_input("Enter a twitter screen name to harvest: "))
count = int(raw_input("How many favorites would you like? (max 3200): "))
lastround = 0

#subdivide all of the tweets to comply with twitter request rules
if count <= 200:
	endrange = 1
	rounds = 1
else:
	#also need to figure out how to determine how many favorites there are and how to stop when no more are coming back
	rounds = count/200.0
	#find how many are left if not an even multiple of 200 for that last round
	lastround = count%200
	#round up the endrage if there is a partial round
	endrange = int(math.ceil(rounds))
	count = 200
starting_tweet_id = 0
print "\n"
time.sleep(1)
print "well chosen..."
time.sleep(2)
print "Parsing favorites from: " + user
if lastround == 0:
	print str(rounds) + " rounds of 200"
else:
	print str(math.trunc(rounds)) + " rounds of 200 and one round of " + str(lastround)
print "\n"

#file of tweets text for use later
fo = open(user + ".txt", "wb")
fo.write("File of favorites from " + user + ":\n\n");
fo.close()

#file of tweet links for stuff
fl = open(user+ "_links" + ".txt", "wb")
fl.write("File of links from " + user + ":\n\n");
fl.close()

howlong = 0

for i in range(0, endrange): ## iterate through all tweets at 200 per round
    ## tweet extract method with the last list item as the max_id
	if starting_tweet_id == 0:
		try:
			user_faves = twitter.get_favorites(screen_name=user, count=count)
		except:
			print "You are not authorized to view this user, they probably have a private profile. The jerks..."
			break
	else:
		try:
			if howlong == endrange:
				user_faves = twitter.get_favorites(screen_name=user, count=count, max_id = starting_tweet_id)
			else:
				user_faves = twitter.get_favorites(screen_name=user, count=lastround, max_id = starting_tweet_id)
		except:
			print "You are not authorized to view this user, they probably have a private profile. The jerks..."
			break
	
	## pretty printing used for troublshooting and finding further parts of a tweet to use
	#pprint.pprint(user_faves)

	for tweet in user_faves:
		# run through the returned tweets and print out the text, the user, and the link.
		# printing out to two files for now. one for text and one for links. Need to work on making this a noSQL database or a flat file
		
		with codecs.open(user + ".txt", "a", encoding='utf-8') as f:
			f.write(str(tweet['id']) + "|" + tweet['text'] + "|" + "Tweeted by: " + tweet['user']['name'] + " (" + tweet['user']['screen_name'] + ")" + "\n")

		with codecs.open(user + "_links" + ".txt", "a", encoding='utf-8') as g:
			try:
				g.write(tweet['entities']['urls'][0]['expanded_url'] + "\n")
			except:
				continue
		
		#print tweet['id'] ##print the id value
		print tweet['text'] ## print the tweet
		#print "\n"
		print "Tweeted by: " + tweet['user']['name'] + " (" + tweet['user']['screen_name'] + ")"

		# error catching in case there is no link...
		try:
			# add logic here to write all links found to a file, also logic to check if a youtube link for another file
			print "Link: " + tweet['entities']['urls'][0]['expanded_url']
		except:
			print "no link"
		print "\n"

		# Updating the tweet_id for the next batch of pulls, using the nifty -1 trick from twitter to eliminate duplicates
		starting_tweet_id = tweet['id'] -1
	
	#update the current round and check to see if we are done. If done, print out some helpful info and exit.
	howlong = howlong+1
	print "\n"
	print "Completed parsing round " + str(howlong) + " of " + str(endrange)
	if howlong == endrange:
		print "Parsing completed. \nSee " + user + ".txt for all tweets in a pipe delimited format. \nSee " + user + "_links.txt for all links from faves." 
		break
	else:
		print "Waiting 60 seconds to avoid twitter usage caps..."
		print "\n"
		time.sleep(60)

#print starting_tweet_id

# still need to build the code to grab screenshots of all of the web links found in the parsing (add some logic to determine if the page can load)
# in addition need to make some logic to write out youtube links to an additional file for usage in the youtube downloader