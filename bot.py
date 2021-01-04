import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from configparser import ConfigParser
import os
import random

intents = discord.Intents.default()
#intents.members = True
bot = commands.Bot(command_prefix='/',intents=intents)
slash = SlashCommand(client=bot,auto_register=True,auto_delete=True)

guild_ids = [673014590862393385]
config = ConfigParser()

def configRequest(cat,set,val):
    """Handles config change requests. All inputs must be entered as a string.

    `cat`: Catergory setting is in

    `set`: Setting to update

    `val`: Desired value for setting
    """
    config.read('config.ini')
    if cat not in config:
        config.add_section(cat)
    config.set(cat,set,val)
    with open('config.ini','w') as update:
        config.write(update)

@bot.event
async def on_ready():
    print('Internal Report Check: Logged in as {0.user}'.format(bot))



@slash.slash(name='mark',description='Designates the current channel for posting to Twitter',guild_ids=guild_ids)
async def _mark(ctx):
    await ctx.send(content='Placeholder')

@slash.slash(
    name='toggle',
    description='Sets message forwarding to Twitter on or off',
    guild_ids=guild_ids,
    options=[{
        'name':'bool',
        'description': 'Value of toggle',
        'type': 5,
        'required': 'True'
    }])
async def _toggle(ctx: SlashContext, value: bool):
    configRequest('Server','toggle',str(value))
    await ctx.send(content=f'Message forwarding set to `{value}`!',complete_hidden=True)

@slash.slash(name='optin',description='Opt into the bot\'s Twitter functionality',guild_ids=guild_ids)
async def _optin(ctx):
    configRequest(str(ctx.author),'opt','True')
    await ctx.send(content='You have opted into having your messages tweeted out!',complete_hidden=True)

@slash.slash(name='optout',description='Opt out of the bot\'s Twitter functionality',guild_ids=guild_ids)
async def _optout(ctx):
    configRequest(str(ctx.author),'opt','False')
    await ctx.send(content='You have opted out of having your messages tweeted out.',complete_hidden=True)



bot.run(os.getenv('TOKEN'))