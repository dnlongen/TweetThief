'''
TweetThief v0.1
Source: https://github.com/dnlongen/TweetThief
Author: David Longenecker
Author email: david@securityforrealpeople.com 
Author Twitter: @dnlongen
Requires tweepy, the Twitter API module for Python, available from https://github.com/tweepy/tweepy
Requires an application token for the Twitter API. See https://dev.twitter.com/oauth/overview/application-owner-access-tokens for documentation, and https://apps.twitter.com to generate your tokens

Note that the search results at twitter.com may return historical results while the Search API usually only serves tweets from the past week. See https://dev.twitter.com/rest/public/search
'''

import argparse, tweepy, sys, codecs, time

#########################################################################
# Replace the below values with your own, from https://apps.twitter.com #
consumer_key = <your consumer key>
consumer_secret = <your consumer secret>
access_token = <your access token>
access_token_secret = <your access token secret>
#########################################################################

# Define supported parameters and default values
parser = argparse.ArgumentParser(description='Find copied but not attributed tweets. TweetThief retrieves the most recent tweets from a specific Twitter user, then searches Twitter for other tweets that are exact copies but are not retweets.')
parser.add_argument('-a', '--alias', dest='twitter_alias', required=True, help='Twitter alias whose tweets to analyze')
parser.add_argument('-n', '--numtweets', default=20, type=int, help='Maximum number of tweets to analyze for specified Twitter user; default 20')
parser.add_argument('-l', '--loose-match', dest='loose_match', default=False, action='store_true', help='Loose matching. By default, TweetThief matches only an exact copy of the full text of a tweet; loose matching will match if the copy contains the original tweet. For example, if the original tweet is "Help Me" and the copy is "Help Me Rhonda" TweetThief normally will not report this as a match, but in loose-match mode it will.')
parser.add_argument('-p', '--proxy', default='', required=False, help='HTTPS proxy to use, if necessary, in the form of https://proxy.com:port')
args=parser.parse_args()
twitter_load=args.numtweets
twitter_list=[args.twitter_alias]
https_proxy=args.proxy
loose_match=args.loose_match

#Uncomment for Python 2:
#if sys.stdout.encoding != 'cp850':
#  sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'xmlcharrefreplace')
#if sys.stderr.encoding != 'cp850':
#  sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'xmlcharrefreplace')

#Uncomment for Python 3:
if sys.stdout.encoding != 'cp850':
  sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
if sys.stderr.encoding != 'cp850':
  sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

def parse_twitter(twitter_user):
    status        = ""
    for status in api.user_timeline(twitter_user,count=twitter_load):
        # since_id returns statuses more recent than specified ID; max_id returns statuses earlier than specified ID
        # no native way to filter user_timeline based on a time window?
        orig_user = status.user.screen_name
        orig_text = status.text
        orig_id   = str(status.id)
        orig_date = time.strftime("%Y-%b-%d %H:%M", time.strptime(str(status.created_at),"%Y-%m-%d %H:%M:%S"))
        orig_link = "https://twitter.com/" + orig_user + "/status/" + str(status.id)
        if (status.retweeted): continue # no sense in checking for matches to something I retweeted
        if (not status.entities["urls"] == []): # if there are urls, expand them
          for url in status.entities["urls"]: orig_text=orig_text.replace(url["url"], url["expanded_url"])
        try:
          for repeat in api.search("\"" + orig_text + "\""):
            repeat_user = repeat.user.screen_name
            if (repeat_user.lower() == orig_user.lower()): continue # skip my own tweet, looking for duplicates by others
            if (repeat.text[:2]=="RT"): continue # not interested in legit retweets, but in uncredited copies
            repeat_text = repeat.text
            repeat_id   = str(repeat.id)
            repeat_date = time.strftime("%Y-%b-%d %H:%M", time.strptime(str(repeat.created_at),"%Y-%m-%d %H:%M:%S"))
            repeat_link = "https://twitter.com/" + repeat_user + "/status/" + repeat_id
            if (not repeat.entities["urls"] == []): # if there are urls, expand them
              for url in repeat.entities["urls"]: repeat_text=repeat_text.replace(url["url"], url["expanded_url"])
            if (not repeat_text==orig_text and not loose-match): continue # make sure complete original and new tweets are an exact match
            print("*******************")
            print("Original tweet: ")
            print("Status ID " + orig_id + " sent at " + orig_date + " by " + orig_user)
            print("Tweet body: \"" + orig_text + "\"")
            print("Status link: " + orig_link)
            print("")
            print("Repeated tweet: ")
            print("Status ID " + repeat_id + " sent at " + repeat_date + " by " + repeat_user)
            print("Tweet body: \"" + repeat_text + "\"")
            print("Status link: " + repeat_link)
            print("*******************\n")
        except tweepy.TweepError as e:
          # 429 means rate-limited
          if str(e).find("status code = 429"): 
            print("Twitter API rate-limited; try again in a few minutes.")
            print("The Twitter API rate-limits requests within a 15-minute window.")
            print("Refer to https://dev.twitter.com/rest/public/rate-limiting for more information.")
            break
          print("Twitter API error. Message:")
          print(str(e))
    print("Finished processing user " + twitter_user)


#################################################################################################
# Main body
#################################################################################################

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,proxy=https_proxy)
for twitter_user in twitter_list:
    # With each Twitter handle, run through the parser routine
    # Current cmdline parameters allow for only one Twitter handle; this is to enable future enhancement
    parse_twitter(twitter_user)
