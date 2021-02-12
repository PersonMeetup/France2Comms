#!/usr/bin/env python
import discord
import requests
from TwitterAPI import TwitterAPI
import os; import re
import logging
from dotenv import load_dotenv
load_dotenv()

api = TwitterAPI(os.getenv('TWITTER_CONKEY'),os.getenv('TWITTER_CONSECRET'),os.getenv('TWITTER_TOKENKEY'),os.getenv('TWITTER_TOKENSECRET'))

class relay:
    """Twitter API handler."""

    def tweet(message):
        tweet = api.request('statuses/update', {'status':message})
        return tweet.status_code

    def mediaTweet(message):
        file = open('./image.png', 'rb')
        data = file.read()
        r = api.request('media/upload', None, {'media': data})
            #print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE: ' + r.text)

        if r.status_code == 200:
            media_id = r.json()['media_id']
            logging.info('Media upload success, Tweeting string...')
            tweet = api.request('statuses/update', {'status':message, 'media_ids':media_id})
            return tweet.status_code

    def apitest():
        r = api.request('statuses/home_timeline', {'count':5})
        return ('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)
