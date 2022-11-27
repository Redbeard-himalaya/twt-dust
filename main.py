#!/usr/local/bin/python

import logging
from twitter import *

class TwtDust:
    def __init__(self,
                 access_token: str = None,
                 access_token_secret: str = None,
                 api_key: str = None,
                 api_key_secret: str = None):
        if access_token is None:
            raise RuntimeError("access_token is None")
        if access_token_secret is None:
            raise RuntimeError("access_token_secret is None")
        if api_key is None:
            raise RuntimeError("api_key is None")
        if api_key_secret is None:
            raise RuntimeError("api_key_secret is None")
        self._t = Twitter(auth=OAuth(access_token, access_token_secret, api_key, api_key_secret))


    # get operation
    def tweets_of_user(self, user: str = "", count: int = 20):
        # references:
        # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-home_timeline
        if count > 200:
            raise RuntimeError("tweets count is larger than 200")
        return self._t.statuses.user_timeline(screen_name=user, count=count)


    # get operation
    def popular_tweets(self, topic: str = "", language: str = "en"):
        # references:
        # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview
        # https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/build-standard-queries
        if language != 'en' and language != 'cs':
            raise RuntimeError("language is not en (English) and cs (Chinese)")
        return self._t.search.tweets(q=topic, result_type='popular', lang=language)['statuses']


    # post operation
    def new_tweet(self, text: str = "Hello, my friends!"):
        # references:
        # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/post-statuses-update
        return self._t.statuses.update(status=txt)


    # post operation
    def reply_tweet(self, at_user: str = None, tweet_id: int = None, text: str = ""):
        # references:
        # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/post-statuses-update
        if at_user is None or tweet_id is None:
            raise RuntimeError("at_user or tweet id is None in tweet reply")
        return self._t.statuses.update(status=f"@{r['user']['screen_name']} {text}",
                                       in_reply_to_status_id=r['id'])


    # post operation
    def retweet(self, tweet_id: int = None):
        return self._t.statuses.retweet(id=tweet_id)


    # helper operation
    def sort_by(self, results = None, field: str = None):
        if not isinstance(results, list):
            raise RuntimeError("results is not list")
        if filed is None:
            raise RuntimeError("filed is None")
        results.sort(key=lambda e: e['favorite_count'], reverse=True)


if __name__ == '__main__':
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(
        description='A tool for: searching twitter timeline and popular tweets; tweeting; retweeting; replying tweets',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('command', metavar='command',
                        choices=['retweet', 'reply', 'search', 'timeline', 'tweet', 'help'],
                        help=
                        'reply:    reply a tweet;\n'
                        'retweet:  retweet a tweet;\n'
                        'search:   search popular tweets of a topic;\n'
                        'timeline: get timeline of a twitter user;\n'
                        'tweet:    create a new tweet;\n'
                        'help:     show this help;')
    parser.add_argument('-c', '--count', type=int, nargs='?', default=20,
                        help='count of tweets returned by timeline')
    parser.add_argument('-i', '--id', type=int, nargs='?', default=None,
                        help='tweet id to reply or retweet')
    parser.add_argument('-l', '--language', type=str, nargs='?', default='en',
                        help='language of the popular tweets')
    parser.add_argument('-p', '--popular', type=str, nargs='?', default='',
                        help='popular tweets to search')
    parser.add_argument('-t', '--text', type=str, nargs='?', default='',
                        help='text content in tweet or tweet\'s reply')
    parser.add_argument('-u', '--user', type=str, nargs='?', default=None,
                        help='the name of tweet user')
    parser.add_argument('--verbose', '-v', action='store_true', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.debug(f"ACCESS_TOKEN:        {os.getenv('ACCESS_TOKEN')}")
    logging.debug(f"ACCESS_TOKEN_SECRET: {os.getenv('ACCESS_TOKEN_SECRET')}")
    logging.debug(f"API_KEY:             {os.getenv('API_KEY')}")
    logging.debug(f"API_KEY_SECRET:      {os.getenv('API_KEY_SECRET')}")

    td = TwtDust(access_token=os.getenv('ACCESS_TOKEN'),
                 access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
                 api_key=os.getenv('API_KEY'),
                 api_key_secret=os.getenv('API_KEY_SECRET'))

    if args.command == 'search':
        retults = td.popular_tweets(topic=args.popular, language=args.language)
        logging.info(f"pupular tweets number: {len(results)}")
    elif args.command == 'timeline':
        results = td.tweets_of_user(user=args.user, count=args.count)
        logging.info(f"user tweets number: {len(results)}")
    elif args.command == 'tweet':
        td.new_tweet(text=args.text)
    elif args.command == 'retweet':
        td.retweet(tweet_id=args.id)
    elif args.command == 'reply':
        td.reply_tweet(at_user=args.user, tweet_id=args.id, text=args.text)
    elif args.command == 'help':
        parser.print_help(sys.stderr)
