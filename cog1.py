# cog.py
import discord
import os
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dotenv import load_dotenv

GUILD = os.getenv('DISCORD_GUILD') # Put your server ID in this array.

class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="test", guild_ids= GUILD)
    async def _test(self, ctx: SlashContext):
        embed = discord.Embed(title="embed test")
        await ctx.send(content="test", embeds=[embed])
    
    @cog_ext.cog_slash(name="ping",
                       description="ping pong ya eh", guild_ids= GUILD)
    async def _ping(self, ctx: SlashContext): 
        await ctx.send(f"Pong! ({round(self.client.latency * 1000)}ms)")

def setup(client):
    client.add_cog(Slash(client))