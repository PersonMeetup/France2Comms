import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from configparser import ConfigParser
import os

intents = discord.Intents.default()
#intents.members = True
bot = commands.Bot(command_prefix='/',intents=intents)
slash = SlashCommand(client=bot,auto_register=True,auto_delete=True)

guild_ids = [673014590862393385]
config = ConfigParser()

def optRequest(opt,user):
    """Handles Twitter function opt requests. All inputs must be entered as a string.

    `opt`: bool value

    `user`: int value repersenting a user ID
    """
    config.read('config.ini')
    if user not in config:
        config.add_section(user)
    config.set(user,'opt',opt)
    with open('config.ini','w') as update:
        config.write(update)

@bot.event
async def on_ready():
    print('Internal Report Check: Logged in as {0.user}'.format(bot))



@slash.slash(name='mark',description='Designates the current channel for posting to Twitter',guild_ids=guild_ids)
async def _mark(ctx):
    await ctx.send(content='Placeholder')

@slash.slash(name='toggle',description='Sets message forwarding to Twitter on or off',guild_ids=guild_ids)
async def _toggle(ctx):
    await ctx.send(content='Placeholder')

@slash.slash(name='optin',description='Opt into the bot\'s Twitter functionality',guild_ids=guild_ids)
async def _optin(ctx):
    optRequest('true',str(ctx.author))
    await ctx.send(content='You have opted into having your messages tweeted out!',complete_hidden=True)

@slash.slash(name='optout',description='Opt out of the bot\'s Twitter functionality',guild_ids=guild_ids)
async def _optout(ctx):
    optRequest('false',str(ctx.author))
    await ctx.send(content='You have opted out of having your messages tweeted out.',complete_hidden=True)



bot.run(os.getenv('TOKEN'))