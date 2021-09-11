# music.py
import discord
import traceback, os, json
import datetime
from discord.colour import Color
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import youtube_dl
from youtube_search import YoutubeSearch

GUILD = [Insert Guild Token Here] # Put your server ID in this array.

class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    link=''

    @cog_ext.cog_slash(name="Play",
                    description="Plays a song for the bois", guild_ids= GUILD)
    async def _play(self, ctx: SlashContext, search):
        song_there = os.path.isfile("song.mp3")
        await ctx.send("playsation In progress")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Eh stahp mon, I havent finished da song yet ya eh. Use the stop command first.")
            return

        global link
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Nolan\'s just yoking')
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if(voice_client and voice_client.is_connected()):
            pass
        else:
            await voiceChannel.connect()

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        }
        
        if 'https://www.youtube.com/watch?v=' in search:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([search])
                    info = ydl.extract_info(search)
                    link = ydl.extract_info(search)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                voice.play(discord.FFmpegPCMAudio("song.mp3"))
                await ctx.send(embed=discord.Embed(title=info.get('title', None),
                               description='love you <3',
                               color=discord.Color.orange())
                 .add_field(name='Duration', value=str(datetime.timedelta(seconds=info.get('duration', None))))
                 .add_field(name='Requested by', value=ctx.author.mention)
                 .set_thumbnail(url=info.get('thumbnail', None)))
        else:
            yt = YoutubeSearch(search, max_results=1).to_json()
            try: 
                yt_id = str(json.loads(yt)['videos'][0]['id'])
                yt_url = 'https://www.youtube.com/watch?v='+yt_id
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([yt_url])
                    info = ydl.extract_info(yt_url)
                    link=ydl.extract_info(yt_url)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                voice.play(discord.FFmpegPCMAudio("song.mp3"))
                await ctx.send(embed=discord.Embed(title=info.get('title', None),
                               description='love you <3',
                               color=discord.Color.orange())
                 .add_field(name='Duration', value=str(datetime.timedelta(seconds=info.get('duration', None))))
                 .add_field(name='Requested by', value=ctx.author.mention)
                 .set_thumbnail(url=info.get('thumbnail', None)))
            
            except:
                pass
                print(traceback.print_exc())
                await ctx.send("No Result bruh")


    @cog_ext.cog_slash(name="leave",
                    description="Leaves the channel sadge :(", guild_ids= GUILD)
    async def _leave(self, ctx: SlashContext):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
            await ctx.send("disconectation complete")
        else:
            await ctx.send("The bot is not connected mon, share the love and invite it ya eh.")


    @cog_ext.cog_slash(name="pause",
                    description="Pause the song so the bois can snuggle", guild_ids= GUILD)
    async def _pause(self, ctx: SlashContext):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send("pausation complete")
        else:
            await ctx.send("no audio is playing let me sing something for yall, so use the play command ya eh.")


    @cog_ext.cog_slash(name="resume",
                    description="Resumes the song after the bois snuggled", guild_ids= GUILD)
    async def _resume(self, ctx: SlashContext):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send("resumation complete")
        else:
            await ctx.send("The audio aint paused mon.")


    @cog_ext.cog_slash(name="stop",
                    description="Stops the song to let the bois concentrate", guild_ids= GUILD)
    async def _stop(self, ctx: SlashContext):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("stopation complete")

    @cog_ext.cog_slash(name="NowPlaying",
                       description="Displays what your playing ya eh", guild_ids= GUILD)
    async def _nowplaying(self, ctx: SlashContext):
        global link
        try:
            song_there = os.path.isfile("song.mp3")
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            info=link
            await ctx.send(embed=discord.Embed(title=info.get('title', None),
                            description='love you <3',
                            color=discord.Color.orange())
                .add_field(name='Duration', value=str(datetime.timedelta(seconds=info.get('duration', None))))
                .add_field(name='Requested by', value=ctx.author.mention)
                .set_thumbnail(url=info.get('thumbnail', None)))

def setup(client):
    client.add_cog(MusicBot(client))
