TweetThief
=============

Who is stealing your tweets?

* Written by David Longenecker
* Twitter: @dnlongen
* Email: david (at) securityforrealpeople.com
* More info: http://www.securityforrealpeople.com/tweetthief

I've noticed a handful of times where one of my tweets, or tweets I recognize from someone else, are duplicated (not retweeted) verbatim by apparent Twitter bots. It struck a curious chord for me, so this weekend I wrote up a tool to look for what I call "parrot accounts" - Twitter accounts that generate no original content, but merely copy others'.

When given the name of a target user (for instance, your own), tweetthief retrieves the most recent tweets by that account. By default it looks at your most recent 20 tweets, but that can be adjusted with the -n parameter. It then searches to see if anyone else has tweeted the exact same thing. It outputs the original and copied tweets, with the Twitter handle and exact posting time for each.

Supply tweetthief with a Twitter alias (your "@name") via the -a argument.

If Internet access requires a proxy, supply it with the parameter -p, in the form of https://proxy.url:port, for instance, -p https://proxy.abc.com:8080

Twitter converts every url into a "t.co" shortlink. The same url tweeted again later will get a different shortlink. TweetThief handles this by examining the url entity, and replacing the t.co shortlink with the expanded url provided by the Twitter API.

The Twitter API is rate-limited, as described at https://dev.twitter.com/rest/public/rate-limiting. If you get a rate-limit error running tweetthief, try again with a smaller -n, or wait a few minutes.

I can think of a few possible motivations for these parrot accounts:
* Fake accounts used in "buy more followers" scams
* Real accounts trying to boost their own followers by claiming others' thoughts for their own
* Something akin to the faux LinkedIn accounts that were reported to be mapping out infosec people's social graphs
* Botnet command and control channels, hiding malicious instructions in innocuous-looking copied tweets
* Or something completely different

Requirements:
=============

* Requires tweepy, the Twitter API module for Python, available from https://github.com/tweepy/tweepy
* Requires an application token for the Twitter API. Refer to documentation at https://dev.twitter.com/oauth/overview/application-owner-access-tokens, and set up your own app-specific tokens at https://apps.twitter.com
 
Note that the search API typically serves up only tweets from the last week or so, and that it is "tuned" toward most relevant results rather than most complete results. I have found some limited cases where the search API does not return results for a search, even though I created a duplicate tweet to search for. YMMV.

Usage:
=============

```
usage: tweetthief.py [-h] -a TWITTER_ALIAS [-n NUMTWEETS] [-l] [-p PROXY]

Find copied but not attributed tweets. Tweetthief retrieves the most recent
tweets from a specific Twitter user, then searches Twitter for other tweets
that are exact copies but are not retweets.

optional arguments:
  -h, --help            show this help message and exit
  -a TWITTER_ALIAS, --alias TWITTER_ALIAS
                        Twitter alias whose tweets to analyze
  -n NUMTWEETS, --numtweets NUMTWEETS
                        Maximum number of tweets to analyze for specified
                        Twitter user; default 20
  -l, --loose-match     Loose matching. By default, tweetthief matches only an
                        exact copy of the full text of a tweet; loose matching
                        will match if the copy contains the original tweet.
                        For example, if the original tweet is "Help Me" and
                        the copy is "Help Me Rhonda" tweetthief normally will
                        not report this as a match, but in loose-match mode it
                        will.
  -p PROXY, --proxy PROXY
                        HTTPS proxy to use, if necessary, in the form of
                        https://proxy.com:port
```

Change Log:
=============

* v0.2 Added --loose-match option to search for copied tweets with a less-strict match
* v0.1 Original release.

Errata:
=============

* The Twitter API search module serves up only tweets from the last week or so, and is "tuned" toward most relevant results rather than most complete results. I have found some limited cases where the search API does not return results for a search, even though I created a duplicate tweet to search for. YMMV.
