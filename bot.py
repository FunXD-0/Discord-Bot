# bot.py
import discord
import os
from discord.ext import commands
from discord_slash import SlashCommand # Importing the newly installed library.

client = commands.Bot(command_prefix="]", intents=discord.Intents().all())
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True) # Declares slash commands through the client.

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="Hackerman"))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That aint a command that exists fam')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You aint got the perms bruh')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Something big was successfully inserted')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Successfully reloaded ' + extension + ' UwU')

@client.command()
async def reloadall(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            client.load_extension(f'cogs.{filename[:-3]}')
    await ctx.send('reload complete MWAHAHAHAHAHAHA')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('Insert Discord Bot Token Here')
