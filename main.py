#!/usr/local/bin/python

import logging
import random
import string
from time import sleep
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
        return self._t.statuses.update(status=text)


    # post operation
    def reply_tweet(self, at_user: str = None, tweet_id: int = None, text: str = ""):
        # references:
        # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/post-statuses-update
        if at_user is None or tweet_id is None:
            raise RuntimeError("at_user or tweet id is None in tweet reply")
        return self._t.statuses.update(status=f"@{at_user} {text}",
                                       in_reply_to_status_id=tweet_id)


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


class CommandHandler:
    def __init__(self, td: TwtDust = None):
        if td is None:
            raise RuntimeError("TwtDust object is None")
        self._td = td


    def _trick_head(self):
        return ''.join(random.sample(string.ascii_lowercase, 8)) + ' '


    def _print_result(self, result):
        logging.info(f" id[{result['id']}]"
                     f" https://twitter.com/i/web/status/{result['id']}"
                     f" created_at[{result['created_at']}]"
                     f" {result['user']['screen_name']}")
        
    def _print_results(self, results):
        for r in results:
            self._print_result(r)
        logging.info(f"total: {len(results)}")


    def timeline(self, user_name: str = None, count: int = 20):
        results = self._td.tweets_of_user(user=user_name, count=count)
        logging.info(f"user: {user_name}")
        self._print_results(results)


    def search(self, topic: str = '', lang: str = 'en'):
        results = td.popular_tweets(topic=topic, language=lang)
        logging.info(f"topic: {topic}")
        self._print_results(results)


    def tweet(self, text: str = ''):
        result = td.new_tweet(text=text)
        self._print_result(result)


    def retweet(self,
                tweet_id: int = None,
                user: str = None,
                count: int = 20,
                topic: str = '',
                lang: str = 'en',
    ):
        if tweet_id is not None:
            # retweet one tweet
            logging.info(f"retweet: https://twitter.com/i/web/status/{tweet_id}")
            result = self._td.retweet(tweet_id=tweet_id)
            self._print_result(result)
        elif user is not None:
            # retweet tweets of a user
            logging.info(f"retweet user: {user}")
            results = self._td.tweets_of_user(user=user, count=count)
            for r in results:
                try:
                    ret = self._td.retweet(tweet_id=r['id'])
                    self._print_result(ret)
                except TwitterHTTPError as e:
                    if e.response_data['errors'][0]['code'] == 327:
                        logging.warning(f" {e.response_data['errors'][0]['message']}"
                                        f" https://twitter.com/i/web/status/{r['id']}")
                finally:
                    sleep(random.randint(5,20))
        else:
            # retweet tweets of a topic
            logging.info(f"retweet {lang} topic: {topic}")
            results = self._td.popular_tweets(topic=topic, language=lang)
            for r in results:
                try:
                    ret = self._td.retweet(tweet_id=r['id'])
                    self._print_result(ret)
                except TwitterHTTPError as e:
                    if e.response_data['errors'][0]['code'] == 327:
                        logging.warning(f"{e.response_data['errors'][0]['message']} [{r['id']}]")
                finally:
                    sleep(random.randint(5,20))


    def reply(self,
              at_user: str = None,
              tweet_id: int = 0,
              topic: str = '',
              lang: str = 'en',
              user_name: str = None,
              count: int = 20,
              text: str = '',
    ):
        if at_user is None and tweet_id is None:
            # reply to a topic tweets
            logging.info(f"reply to {lang} topic: {topic}")
            results = self._td.popular_tweets(topic=topic, language=lang)
            for r in results:
                ret = self._td.reply_tweet(at_user=r['user']['screen_name'],
                                           tweet_id=r['id'],
                                           text=self._trick_head() + text)
                self._print_result(ret)
                sleep(random.randint(15,40))
        elif tweet_id is None:
            # reply to a user's tweets
            logging.info(f"reply to user: {at_user}")
            results = self._td.tweets_of_user(user=at_user, count=count)
            for r in results:
                ret = self._td.reply_tweet(at_user=r['user']['screen_name'],
                                           tweet_id=r['id'],
                                           text=self._trick_head() + text)
                self._print_result(ret)
                sleep(random.randint(15,40))
        else:
            # reply to one tweet
            logging.info(f"reply to tweet: https://twitter.com/i/web/status/{tweet_id}")
            result = self._td.reply_tweet(at_user=at_user,
                                          tweet_id=tweet_id,
                                          text=self._trick_head() + text)
            self._print_result(result)


if __name__ == '__main__':
    import argparse
    import os
    import sys

    example_text = '''example:

 main.py help
 main.py timeline -u <user_name> -c <count>
 main.py search -p <topic> -l [cs|en]
 main.py tweet -t <text>
 main.py retweet -i <id>
 main.py retweet -u <user_name> [-c count]
 main.py retweet -p <topic> [-l [en|cs]]
 main.py reply -t <text> -u <user_name> -i <id>
 main.py reply -t <text> -u <user_name> [-c count]
 main.py reply -t <text> -p <topic> [-l [en|cs]]
'''

    parser = argparse.ArgumentParser(
        description='A tool for: searching twitter timeline and popular tweets; tweeting; retweeting; replying tweets',
        epilog=example_text,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('command', metavar='command',
                        choices=[
                            'reply',
                            'retweet',
                            'search',
                            'timeline',
                            'tweet',
                            'help',
                        ],
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
    else:
        logging.getLogger().setLevel(logging.INFO)

    logging.debug(f"ACCESS_TOKEN:        {os.getenv('ACCESS_TOKEN')}")
    logging.debug(f"ACCESS_TOKEN_SECRET: {os.getenv('ACCESS_TOKEN_SECRET')}")
    logging.debug(f"API_KEY:             {os.getenv('API_KEY')}")
    logging.debug(f"API_KEY_SECRET:      {os.getenv('API_KEY_SECRET')}")

    td = TwtDust(access_token=os.getenv('ACCESS_TOKEN'),
                 access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
                 api_key=os.getenv('API_KEY'),
                 api_key_secret=os.getenv('API_KEY_SECRET'))
    hd = CommandHandler(td)

    if args.command == 'search':
        hd.search(topic=args.popular, lang=args.language)
    elif args.command == 'timeline':
        hd.timeline(user_name=args.user, count=args.count)
    elif args.command == 'tweet':
        hd.tweet(text=args.text)
    elif args.command == 'retweet':
        hd.retweet(tweet_id=args.id,
                   user=args.user,
                   count=args.count,
                   topic=args.popular,
                   lang=args.language)
    elif args.command == 'reply':
        hd.reply(at_user=args.user,
                 tweet_id=args.id,
                 topic=args.popular,
                 lang=args.language,
                 count=args.count,
                 text=args.text)
    elif args.command == 'help':
        parser.print_help(sys.stderr)
