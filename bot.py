import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import os

intents = discord.Intents.default()
#intents.members = True
bot = commands.Bot(command_prefix='/',intents=intents)
slash = SlashCommand(client=bot,auto_register=True,auto_delete=True)
guild_ids = [673014590862393385]

@bot.event
async def on_ready():
    print('Internal Report Check: Logged in as {0.user}'.format(bot))

@slash.slash(name='test',description='Test to check basic functionality',guild_ids=guild_ids)
async def _test(ctx: SlashContext):
    await ctx.send(content='Test')

bot.run(os.getenv('TOKEN'))