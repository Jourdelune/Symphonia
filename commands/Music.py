import re
from utils.utils import *
import discord
import lavalink
from discord.ext import commands
from youtubesearchpython import *
from dateutil.relativedelta import relativedelta
from youtubesearchpython import *
from discord import utils
from discord import Embed
import re
import math
import time
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="bc1f01e2722747699311b953fb45e8df",
                                                           client_secret="9a2fa3f8100744d7a984bf67a256b5ad"))

url_rx = re.compile(r'https?://(?:www\.)?.+')

track_del=None
list_play={}
server_replay=[]
dict_ctx={}
list_ctx=[]
last_name={}
statut_musique=[]
timetemps={}
pause={}
guild_value={}
in_skip={}
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'): 
            bot.lavalink = lavalink.Client(814500334806237225)
            bot.lavalink.add_node("localhost", self.bot.lavalinkport, self.bot.lavalinkpass, 'na', 'default-node')
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')
     

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)
    

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"An error has occurred, please report it on the [support discord server](https://discord.gg/qaQtvNmdm5).\n```{error}```")
            await ctx.send(embed=embed)
            raise error
           
     

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play', 'skip')
       
        
        if not ctx.author.voice or not ctx.author.voice.channel:
            if should_connect:
                print(ctx.command.name)
                return await ctx.send("<:error:805750300450357308> **You are not connected to a voice channel.**")

        if not player.is_connected:
            if not should_connect:
                return await ctx.send("<:error:805750300450357308> **Not connected.**")

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('<:error:805750300450357308> **I need the `CONNECT` and `SPEAK` permissions.**')

            player.store('channel', ctx.channel.id)
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel)
        else:
            pass
    


    async def track_hook(self, event):
        if isinstance(event, lavalink.events.TrackStuckEvent):
            print(" ah ah")
        if isinstance(event, lavalink.events.QueueEndEvent):
            print("stop")
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on repsources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            player = self.bot.lavalink.player_manager.get(guild_id)
            print(player.current)
            await guild.change_voice_state(channel=None)
                    
            
        
        
            
    @commands.command(aliases=['v'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def volume(self, ctx, query: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)
        
        await player.set_volume(query)
        if query == 0:
            await ctx.send(":mute: **Changed volume to {}%**".format(query))
        else:
            await ctx.send(":loud_sound: **Changed volume to {}%**".format(query))
        
     
    @commands.command()
    async def music(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await self.bot.lavalink.player_manager.destroy(ctx.guild.id)
        
        
    @commands.command(aliases=['p'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def play(self, ctx, *, query: str):
        if len(query) >= 100:
            await ctx.send("<:error:805750300450357308> **You cannot put more than 100 characters.**")
            return
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)

            return
        
        if not (ctx in list_ctx):
            list_ctx.append(ctx)
        if not (ctx in dict_ctx):
            dict_ctx[ctx.guild.id]=ctx
        if not ctx.author.voice:
            return
        
        save=query
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        query = query.strip('<>')
        message = await ctx.send(f"<:search:805751542920773633> **currently researching** `{query}`.")
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

    
        results = await player.node.get_tracks(query)
        conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                       password=database_password(),
                                       database=database_name())

        cursor = conn.cursor()
        cursor.execute(f"""SELECT comportement_custom FROM music_guild WHERE guild_id={ctx.guild.id}""")
        value = cursor.fetchone()
        conn.close()
        if value is None:
            value = False
        else:
            value=value[0]

        if not results or not results['tracks']:
            try:
                results = sp.track(save)
                save = f"ytsearch:{results['album']['artists'][0]['name']} {results['name']}"
                results = await player.node.get_tracks(save)
                if not results or not results['tracks']:
                    return await message.edit(content="<:error:805750300450357308> **No music found.**") if message else await ctx.send(content="<:error:805750300450357308> **No music found.**")
            except:
                return await message.edit(content="<:error:805750300450357308> **No music found.**") if message else await ctx.send(content="<:error:805750300450357308> **No music found.**")
            
       
        
        
       
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
      
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
      
            playing_after=0
            for i in player.queue:
                playing_after+=i.duration 
            search = VideosSearch(track["info"]["uri"], limit = 1)
            search=search.result()['result']
            embed = discord.Embed(color=embed_color(ctx.guild.id), description=f'[{track["info"]["title"]}]({track["info"]["uri"]})')
            embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
            if 'https://www.youtube.com/' in track["info"]["uri"]:
                embed.set_thumbnail(url=search[0]['thumbnails'][0]['url'])       
            embed.add_field(name="Author", value=track["info"]['author'], inline=True)        
            embed.add_field(name="Duration", value=convert_duration(track["info"]['length']/1000) if track["info"]["isStream"] == False else ":red_circle: stream", inline=True)
            embed.add_field(name="Estimated time until playing", value=convert_duration(playing_after/1000) if player.current is None else convert_duration(playing_after/1000+track["info"]['length']/1000), inline=True)
            embed.add_field(name="position", value=len(player.queue) if player.current is None else len(player.queue)+1, inline=True)
            embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/805066192834396210/813037403731918908/Songs.png",
                                 text=f"Song")
            
            await message.edit(content=None, embed=embed)
            
        else:   
            track = results['tracks'][0]
            
            embed = discord.Embed(color=embed_color(ctx.guild.id), description=f'[{track["info"]["title"]}]({track["info"]["uri"]})')

            search = VideosSearch(track["info"]["uri"], limit = 1)
            search=search.result()['result']
            
            playing_after=0     
            for i in player.queue:
                playing_after+=i.duration
           
            embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
  
            if 'https://www.youtube.com/' in track["info"]["uri"]:
                embed.set_thumbnail(url=search[0]['thumbnails'][0]['url']) 
            embed.add_field(name="Author", value=track["info"]['author'], inline=True)        
            embed.add_field(name="Duration", value=convert_duration(track["info"]['length']/1000) if track["info"]["isStream"] == False else ":red_circle: stream", inline=True)
            embed.add_field(name="Estimated time until playing", value=convert_duration(playing_after/1000) if player.current is None else convert_duration(playing_after/1000+track["info"]['length']/1000), inline=True)
            embed.add_field(name="position", value=len(player.queue) if player.current is None else len(player.queue)+1, inline=True)
            embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/805066192834396210/813037403731918908/Songs.png",
                                 text=f"Song")
            

  
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

            await message.edit(content=None, embed=embed)


        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['l', 'dc', 'disconnect'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def leave(self, ctx):    
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("<:error:805750300450357308> **You are not connected in my voice channel.**")
        
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)

        
        player.queue.clear()
        await player.stop()
        await ctx.guild.change_voice_state(channel=None)
        await ctx.send(":arrow_left: **Songs left the voice channel.**")
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, member):
        try:
            if (reaction.message.id in in_skip) is False:
                return
            if member.bot:
                return
            player = self.bot.lavalink.player_manager.get(int(reaction.message.guild.id))
            if int(member.voice.channel.id) == int(player.channel_id):
                value=in_skip[reaction.message.id][0]
                in_skip[reaction.message.id]=[value-1, in_skip[reaction.message.id][1]]
                message = in_skip[reaction.message.id][1]
                nbm_bot=0
                for i in member.voice.channel.members:
                    if i.bot:
                        nbm_bot+=1
                nbm_bot = len(member.voice.channel.members)-nbm_bot
                try:
                    await message.edit(content=f":track_next: `{in_skip[reaction.message.id][0]}/{math.ceil(nbm_bot/2)}` **press reaction to vote**")
                except:
                    channel = self.bot.get_channel(reaction.message.channel.id)
                    return await channel.send("<:error:805750300450357308> **You have deleted the message.**")
        except:
            channel = self.bot.get_channel(reaction.message.channel.id)
            await channel.send("<:error:805750300450357308> **No music played.**")
            
                    
      
            
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            if (payload.message_id in in_skip) is False:
                return
        
            if payload.member.bot:
                    return
            
            player = self.bot.lavalink.player_manager.get(payload.guild_id)
            if int(payload.member.voice.channel.id) == int(player.channel_id):
                value=in_skip[payload.message_id][0]
                in_skip[payload.message_id]=[value+1, in_skip[payload.message_id][1]]
                nbm_bot=0
                for i in payload.member.voice.channel.members:
                    if i.bot:
                        nbm_bot+=1
                nbm_bot = len(payload.member.voice.channel.members)-nbm_bot
     
                if int(in_skip[payload.message_id][0]) >= math.ceil(nbm_bot/2):
                    await player.skip()
                    channel = self.bot.get_channel(payload.channel_id)
                    skipped=player.current
        
                    if skipped is not None:
                        await channel.send(f':track_next: **Skipped** `{skipped["author"]}`')
                    else:
                        await channel.send(f':track_next: **Skipped**')
                    del in_skip[payload.message_id]
                    
               
                else:
                    try:
                        message = in_skip[payload.message_id][1]
                        await message.edit(content=f":track_next: `{in_skip[payload.message_id][0]}/{math.ceil(nbm_bot/2)}` **press reaction to vote**")
                    except:
                        channel = self.bot.get_channel(payload.channel_id)
                        return await channel.send("<:error:805750300450357308> **You have deleted the message.**")
                       
        except:
            channel = self.bot.get_channel(payload.channel_id)
            await channel.send("<:error:805750300450357308> **No music played.**")
            
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    @commands.command()
    async def skip(self, ctx):
        """Skip the current song."""
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
     
   
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        nbm_bot=0
        try:
            for i in ctx.author.voice.channel.members:
                if i.bot:
                    nbm_bot+=1
            nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        except:
            return
        
        permissions = ctx.author.guild_permissions
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            message=await ctx.send(f":track_next: `0/{math.ceil(nbm_bot/2)}` **press reaction to vote**")
            emoji = '\N{THUMBS UP SIGN}'
            in_skip[ctx.message.id]=[0, message]
            await ctx.message.add_reaction(emoji)
            return
            
        
            
        conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                    password=database_password(),
                                    database=database_name())

        cursor = conn.cursor()
        cursor.execute(f"""SELECT comportement_custom FROM music_guild WHERE guild_id={ctx.guild.id}""")
        value = cursor.fetchone()
        conn.close()
        if value is None:
            value = False
        else:
            value=value[0]
            
        skipped=player.current
        
        if value == "True":
            emoji = "✅"
            await ctx.message.add_reaction(emoji)
        else:
            if skipped is not None:
                await ctx.send(f':track_next: **Skipped** `{skipped["author"]}`')
            
        await player.skip()
      
    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def stop(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("<:error:805750300450357308> **You are not connected in my voice channel.**")
        
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)
        
        if player.current is not None:
            player.queue.clear()
            await player.stop()
        else:
            return await ctx.send("<:error:805750300450357308> **No musique played.**")
            
        conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                    password=database_password(),
                                    database=database_name())

        cursor = conn.cursor()
        cursor.execute(f"""SELECT comportement_custom FROM music_guild WHERE guild_id={ctx.guild.id}""")
        value = cursor.fetchone()
        conn.close()
        if value is None:
            value = False
        else:
            value=value[0]
            
        if value == "True":
            emoji = "✅"
            await ctx.message.add_reaction(emoji)
        else:
            await ctx.send("✅ **Music Stopped**")
       
      
    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def pause(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            return await ctx.send(embed=embed, delete_after=3.0)
           
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("<:error:805750300450357308> **You are not connected in my voice channel.**")
        
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)
        
        await player.set_pause(True)
        skipped=player.current
       
        if skipped is not None:
            await ctx.send(f':pause_button: **Paused** `{skipped["author"]}`')
        
    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def resume(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            return await ctx.send(embed=embed, delete_after=3.0)
           
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("<:error:805750300450357308> **You are not connected in my voice channel.**")
        
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)
        
        await player.set_pause(False)
        skipped=player.current

        if skipped is not None:
            await ctx.send(f':arrow_forward: **Resumed** `{skipped["author"]}`')
            
            
    @commands.command()
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
    async def loop(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("<:error:805750300450357308> **You are not connected in my voice channel.**")
        
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)
        
        current = player.current
        song = player.repeat
        
        if song:
            player.repeat = False
            await ctx.send(f":infinity: **Disabled loop for** `{current.title}`")
            
            
            
        else:
            player.repeat = True
            await ctx.send(f":infinity: **Enabled loop for** `{current.title}`")
            

    @commands.command(aliases=['s'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def shuffle(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("<:error:805750300450357308> **You are not connected in my voice channel.**")
        
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)
        
        if player.shuffle:
            player.shuffle=False
            await ctx.send(":revolving_hearts: ** disabled queue shuffle!**")
        else:
            player.shuffle=True
            await ctx.send(":revolving_hearts: ** enabled queue shuffle!**")
        
    @commands.command(aliases=['q'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def queue(self, ctx, page: int = 1):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'
        
        embed = discord.Embed(colour=embed_color(ctx.guild.id),
                          description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['r'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def remove(self, ctx, index: int):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("<:error:805750300450357308> **You are not connected in my voice channel.**")
        
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)
        
        a=player.queue
        try:
            del player.queue[int(index)]
        except IndexError:
            return await ctx.send(f"<:error:805750300450357308> **Bad Index**\n`do remove [index] and index is an integer (position of the music in the queue)`")

        await ctx.send(f":wastebasket: **Removed** the song **from queue**")
        
    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def replay(self, ctx, seconde: int):
        affiche=seconde
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("<:error:805750300450357308> **You are not connected in my voice channel.**")
        
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)
        
        track=player.current
        if (track.identifier in pause):
            return await ctx.send("<:error:805750300450357308> **You cannot do this action on paused music.**")
        
        if affiche > 0:
            await ctx.send(f":track_next: `{affiche}` **second delay.**")
        else:
            await ctx.send(f":track_previous: `{affiche}` **second delay.**")

        await player.seek(player.position+int(seconde*1000))
  
       
     
    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def np(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.current == None:
            return await ctx.send("<:error:805750300450357308> **No musique played.**")

        try:      
            pourcent = (player.position*100)/player.current.duration
        
            barre="▬"*int((int(pourcent)/5))
            final=""
            error=0
            for i in list(range(20)):
                try:
                    final=final+barre[i]
                except:
                    if error == 0:
                        final=final+":radio_button:"
                    else:
                        final=final+"▬"
                    error+=1     
            stream="stream"
            embed = discord.Embed(color=embed_color(ctx.guild.id), description=f"""**[{player.current.title}]({player.current.uri})**\n`{convert_duration(player.position/1000)}/{convert_duration(player.current.duration/1000) if track["info"]["isStream"] == False else stream}`\n\n**|{final}|**""")  
        except:
            embed = discord.Embed(color=embed_color(ctx.guild.id), description=f"""**[{player.current.title}]({player.current.uri})**""")

        embed.set_author(name=f"Info", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Author", value=f"{player.current.author}", inline=True)        
        embed.add_field(name="loop", value=f"{player.repeat}", inline=True)
        embed.add_field(name="time", value=f"{convert_duration(player.position/1000)}", inline=True)
        
        await ctx.send(embed=embed)
       

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def bassboost(self, ctx, value: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("<:error:805750300450357308> **You are not connected in my voice channel.**")
        
        permissions = ctx.author.guild_permissions
        nbm_bot=0
        for i in ctx.author.voice.channel.members:
            if i.bot:
                nbm_bot+=1
        nbm_bot = len(ctx.author.voice.channel.members)-nbm_bot
        if nbm_bot == 1 and int(ctx.author.voice.channel.id) == int(player.channel_id) or permissions.manage_channels:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            return await ctx.send(embed=embed, delete_after=3.0)
        
        if value < 0 or value > 100:
            return await ctx.send("<:error:805750300450357308> **The bass cannot exceed 100% or 0%.**")
        if value == 0:
            await player.reset_equalizer()
            await ctx.send(f":speaker: **reset player to** `{value}`**.**")
        else:
            a=value/100
            await player.set_gains((0, a), (1, (value*2)/100))
            await ctx.send(f":loud_sound: **Bass update to** `{value}`**.**")
  
    
def setup(bot):
    bot.add_cog(Music(bot))

    