#!/usr/bin/env python
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from configparser import ConfigParser
import os; import logging
from twitter import relay
from dotenv import load_dotenv
load_dotenv()      #V{filename='status.log',}
logging.basicConfig(format='[%(asctime)s:%(levelname)s] %(message)s', level=logging.INFO)

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='/',intents=intents)
slash = SlashCommand(client=bot,auto_register=True,auto_delete=True)

guild_ids = [673014590862393385]
dev_ids = [149608924394422272,439344743093239810,181130456706580480]
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

# Credit to ╳(͜͡𝓪𝓷𝓖 ⑆#5512 from the discord.py slash command server for this function.
def qualified(f):
    async def wrap(ctx, *args, **kwargs):
        author_id = ctx.author.id if isinstance(ctx.author, discord.Member) else ctx.author

        if author_id in dev_ids:
            return await f(ctx, *args, **kwargs)

        else:
            await ctx.send(content = f"Only The Queen(s) or Person can call this command.", complete_hidden = True)
    return wrap



@bot.event
async def on_ready():
    logging.info('Internal Report Check: Logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    config.read('config.ini')
    # Check two things: 1) "Should I be checking messages right now?"
    #                   2) "Is this in the right channel?"
    if (config.getboolean('Server','toggle') == False) or (message.channel.id != config.getint('Server','channel')):
        logging.debug('Message was posted in the wrong channel, or Twitter functionality is off')
        return

    # Now that the message is confirmed to be in the right channel,
    # let's check to see if the user is opted in.
    if str(message.author.id) in config:
        opt = config.getboolean(str(message.author.id),'opt')
        logging.debug(f'User settings detected: {message.author.id}')
    else:
        opt = config.getboolean('User-Default','opt')
        logging.debug(f'No user settings detected ({message.author.id}), using default')

    if opt == False:
        return
    else:
        logging.info(f'NEW MESSAGE: [{message.content}]')
        responcecode = relay.distweet(message)
        try:
            responcecode == 200
            logging.info('Tweet Successful!')
        except:
            logging.warning("The Tweet didn't go through, AND I HAVE NO IDEA HOW TO FIX THIS PLACE")




@slash.slash(
    name='mark',
    description='Designates either the current or a selected channel for posting to Twitter',
    guild_ids=guild_ids,
    options=[{
        'name':'channel',
        'description': 'ID of desired channel',
        'type': 7,
    }])
@qualified
async def _mark(ctx: SlashContext, channel = None):
    if channel:
        configRequest('Server','channel',str(channel.id))
        await ctx.send(content=f"Set {channel.mention} to have it's messages sent to Twitter.",complete_hidden=True)
        logging.warning(f'Twitter channel ID has been set to {channel.id}!')
    else:
        configRequest('Server','channel',str(ctx.channel.id))
        await ctx.send(content="Set the current channel to have it's messages sent to Twitter.",complete_hidden=True)
        logging.warning(f'Twitter channel ID has been set to {ctx.channel.id}!')

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
@qualified
async def _toggle(ctx: SlashContext, value: bool):
    configRequest('Server','toggle',str(value))
    logging.warning(f'Message forwarding has been set to {value}!')
    await ctx.send(content=f'Message forwarding set to `{value}`!',complete_hidden=True)

@slash.slash(name='optin',description="Opt into the bot's Twitter functionality",guild_ids=guild_ids)
async def _optin(ctx):
    configRequest(str(ctx.author),'opt','True')
    await ctx.send(content='You have opted into having your messages tweeted out!',complete_hidden=True)

@slash.slash(name='optout',description="Opt out of the bot's Twitter functionality",guild_ids=guild_ids)
async def _optout(ctx):
    configRequest(str(ctx.author),'opt','False')
    await ctx.send(content='You have opted out of having your messages tweeted out.',complete_hidden=True)



bot.run(os.getenv('DISCORD_TOKEN'))
