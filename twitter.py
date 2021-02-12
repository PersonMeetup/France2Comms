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

    def distweet(message):
        """Decompiles a `discord.Message` method and posts its content to Twitter"""
        status = message.content
        if message.attachments:
            logging.info(f'Message contains attachment, extracting URL... [{(message.attachments[0]).url}]')
            r = requests.get((message.attachments[0]).url)
            with open('image.png','wb') as f:
                f.write(r.content)

            file = open('./image.png', 'rb')
            data = file.read()
            r = api.request('media/upload', None, {'media': data})
            #print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE: ' + r.text)

            if r.status_code == 200:
                media_id = r.json()['media_id']
                tweet = api.request('statuses/update', {'status':status[:280], 'media_ids':media_id})
                return tweet.status_code

        tweet = api.request('statuses/update', {'status':status[:280]})
        return tweet.status_code

    def apitest():
        r = api.request('statuses/home_timeline', {'count':5})
        return ('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)
