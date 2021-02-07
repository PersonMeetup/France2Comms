import discord
from TwitterAPI import TwitterAPI
import os; import re

api = TwitterAPI(os.getenv('TWITTER_CONKEY'),os.getenv('TWITTER_CONSECRET'),os.getenv('TWITTER_TOKENKEY'),os.getenv('TWITTER_TOKENSECRET'))

class relay:
    """Twitter API handler."""
    
    def distweet(message):
        """Decompiles a `discord.Message` method and posts its content to Twitter"""
        status = message.content
        #if message.attachments:
        #    file = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', message.attachments[0])

        r = api.request('statuses/update', {'status':status[:280]})
        return r.status_code
    
    def apitest():
        r = api.request('statuses/home_timeline', {'count':5})
        return ('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)
