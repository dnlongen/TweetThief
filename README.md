TweetThief
=============

Who is stealing your tweets?

* Written by David Longenecker
* Twitter: @dnlongen
* Email: david (at) securityforrealpeople.com
* More info: http://www.securityforrealpeople.com/tweetthief

Find tweets that are an exact copy of your own, but that are not retweets nor attributed to you. TweetThief retrieves your most recent tweets (by default the most recent 20, but that can be adjusted using the -n command line argument). It then searches Twitter for other tweets with the exact same text.

Supply TweetThief with a Twitter alias (your "@name") via the -a argument.

If Internet access requires a proxy, supply it with the parameter -p, in the form of https://proxy.url:port, for instance, -p https://proxy.abc.com:8080

Twitter converts every url into a "t.co" shortlink. The same url tweeted again later will get a different shortlink. TweetThief handles this by examining the url entity, and replaconf the t.co shortlink with the expanded url provided by the Twitter API.

The Twitter API is rate-limited, as described at https://dev.twitter.com/rest/public/rate-limiting. If you get a rate-limit error running tweetthief, try again with a smaller -n, or wait a few minutes.

Requirements:
=============

* Requires tweepy, the Twitter API module for Python, available from https://github.com/tweepy/tweepy
* Requires an application token for the Twitter API. refer to documentation at https://dev.twitter.com/oauth/overview/application-owner-access-tokens, and set up your own app-specific tokens at https://apps.twitter.com
 
Note that the search API typically serves up only tweets from the last week or so, and that it is "tuned" toward most relevant results rather than most complete results. I have found some limited cases where the search API does not return results for a search, even though I created a duplicate tweet to search for. YMMV.

Usage:
=============

```
usage: tweetthief.py [-h] -a TWITTER_ALIAS [-n NUMTWEETS] [-l] [-p PROXY]

Find copied but not attributed tweets. TweetThief retrieves the most recent
tweets from a specific Twitter user, then searches Twitter for other tweets
that are exact copies but are not retweets.

optional arguments:
  -h, --help            show this help message and exit
  -a TWITTER_ALIAS, --alias TWITTER_ALIAS
                        Twitter alias whose tweets to analyze
  -n NUMTWEETS, --numtweets NUMTWEETS
                        Maximum number of tweets to analyze for specified
                        Twitter user; default 20
  -l, --loose-match     Loose matching. By default, TweetThief matches only an
                        exact copy of the full text of a tweet; loose matching
                        will match if the copy contains the original tweet.
                        For example, if the original tweet is "Help Me" and
                        the copy is "Help Me Rhonda" TweetThief normally will
                        not report this as a match, but in loose-match mode it
                        will.
  -p PROXY, --proxy PROXY
                        HTTPS proxy to use, if necessary, in the form of
                        https://proxy.com:port
```

Change Log:
=============

* v0.1 Original release.

Errata:
=============

* The Twitter API search module serves up only tweets from the last week or so, and is "tuned" toward most relevant results rather than most complete results. I have found some limited cases where the search API does not return results for a search, even though I created a duplicate tweet to search for. YMMV.
