from discord.ext import tasks, commands
import asyncio
import discord
from utils.utils import *
import re
import discord
from dateutil.relativedelta import relativedelta
import DiscordUtils
from numerize import numerize
import mysql.connector
import random

music = DiscordUtils.Music()

server_replay=[]
dict_ctx={}
list_ctx=[]
last_name={}
statut_musique=[]

class Play(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.check_time.start()
        self.check_member.start()
    
    @tasks.loop(seconds=60)
    async def check_member(self):
        for ctx in list_ctx:
            try:
                if len(ctx.voice_client.channel.members) == 1:
                    player = music.get_player(guild_id=ctx.guild.id)
                    if not ctx.voice_client.is_playing():
                        await ctx.voice_client.disconnect()
                        await ctx.send(":arrow_left: **Song' Bot left the channel because no music is played and no one is in the vocal.**")
                    else:
                        if player.now_playing() is not None:
                            song = player.now_playing()
                            if song.is_looping:
                                await player.stop()
                                await ctx.voice_client.disconnect()
                                await ctx.send(":arrow_left: **Song' Bot is disconnected because you have launched a music does not loop without listening to it**")
            except:
                list_ctx.remove(ctx)
                
          
          
    @tasks.loop(seconds=0.5)
    async def check_time(self):
        for ctx in list_ctx:
            if ctx.voice_client is None:
                return
            if ctx.voice_client.is_playing:
                player = music.get_player(guild_id=ctx.guild.id)
                try:
                    song = player.current_queue()[0]
                except:
                    return
                if (ctx.guild.id in last_name):
                    song_object=last_name[ctx.guild.id]
                else:
                    last_name[ctx.guild.id]=song.music_id
                
                song_object=last_name[ctx.guild.id]
              
                if song.music_id != song_object:
                    reset_duration(ctx)
                    last_name[ctx.guild.id]=song.music_id
                else:
                    if (ctx.guild.id in statut_musique):
                        playing_duration(ctx, song.duration)
                    else:
                        playing_duration(ctx, song.duration)
                    
                
            else:
                reset_duration(ctx)
                
        
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def stop(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = music.get_player(guild_id=ctx.guild.id)
        await player.stop()
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
            emoji = '\N{NO ENTRY}'
            await ctx.message.add_reaction(emoji)
        else:
            await ctx.send(":no_entry: **Music Stopped**")
            
        
        
    @commands.command(aliases=['l'])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def leave(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        try:
            await ctx.voice_client.disconnect()
            await ctx.send(":arrow_left: **Songs left the voice channel.**")
        except:
            await ctx.send("<:error:805750300450357308> **The bot is not connected to a voice channel.**")
        
    @commands.command(aliases=['p'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def play(self, ctx, *, url):
        if len(url) >= 100:
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
        
        message = await ctx.send(f"<:search:805751542920773633> **currently researching** `{url}`.")
        player = music.get_player(guild_id=ctx.guild.id)
        if player is not None:
            if len(player.current_queue()) >= 9:
                await ctx.send("<:error:805750300450357308> **The maximum tail is 9 songs.**")
                return
            
        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        
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
        if not ctx.voice_client.is_playing():
            try:
                await player.queue(url, search=True)
            except:
                try:
                    await player.queue(url, bettersearch=True)
                except:
                    await message.edit(content="<:error:805750300450357308> **No music found.**")
                    return
            
            try:
                song = await player.play()
            except:
                await ctx.author.voice.channel.connect(timeout=None)
                song = await player.play()
            if value == "True":
                await message.edit(content=f":metal:**New music played!** `{song.title}`")
            else:
                embed = discord.Embed(color=embed_color(ctx.guild.id), description=f"**[{song.title}]({song.url})**")
                embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=song.thumbnail)
                embed.add_field(name="Autor", value=f"{song.channel}", inline=True)        
                embed.add_field(name="Duration", value=f"{convert_duration(song.duration)}", inline=True)
                embed.add_field(name="Estimated time until playing", value=f"0", inline=True)
                embed.add_field(name="position", value=f"0", inline=True)
                embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/805066192834396210/813037403731918908/Songs.png",
                                 text=f"Song")
            
                await message.edit(content=None, embed=embed)

        else:
            song = await player.queue(url, search=True)
            embed = discord.Embed(color=embed_color(ctx.guild.id), description=f"**[{song.title}]({song.url})**")     
            embed.set_author(name=f"Added to queue", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=song.thumbnail)
            embed.add_field(name="Autor", value=f"{song.channel}", inline=True)
            player = music.get_player(guild_id=ctx.guild.id)
            all_duration=0
            position=0
            for i in player.current_queue():
                if song.url != i.url:
                    all_duration=all_duration+i.duration
                    position+=1
                else:
                    break
            if value == "True":
                await message.edit(content=f":white_check_mark:**Added to queue!** `{song.title}`")
            else:
                embed.add_field(name="Duration", value=f"{convert_duration(song.duration)}", inline=True)
                embed.add_field(name="time until playing", value=f"{convert_duration(all_duration+song.duration)}", inline=True)
                embed.add_field(name="position", value=f"{position}", inline=True)
                embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/805066192834396210/813037403731918908/Songs.png",
                                 text=f"Song")
                await message.edit(content=None, embed=embed)
            
            
        

        
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(timeout=None)
                
            else:
                await ctx.send("<:error:805750300450357308> **You are not connected to a voice channel.**")
        
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def pause(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = music.get_player(guild_id=ctx.guild.id)
        verif=check_mode_pause(ctx)
        if verif == True:
            await ctx.send(f":pause_button: **Music already paused.**")
            return
        mode_pause(ctx, "on")
        try:
            song = await player.pause()
            await ctx.send(f":pause_button: **Paused** `{song.name}`")
        except:
            await ctx.send(f"<:error:805750300450357308> **No music played**")
            
        if not (ctx.guild.id in statut_musique):
            statut_musique.append(ctx.guild.id)
        
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def resume(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        if (ctx.guild.id in statut_musique):
            statut_musique.remove(ctx.guild.id)
        verif=check_mode_pause(ctx)
        if verif == False:
            await ctx.send(f":arrow_forward: **music already being played.**")
            return
        player = music.get_player(guild_id=ctx.guild.id)
        mode_pause(ctx, "off")
        try:
            song = await player.resume()
            await ctx.send(f":arrow_forward: **Resumed** `{song.name}`")
        except:
            await ctx.send(f"<:error:805750300450357308> **No music played**")

    
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
        
        player = music.get_player(guild_id=ctx.guild.id)
        if (ctx.guild.id in server_replay):
            await ctx.send(f"<:error:805750300450357308> **You cannot set a loop on a replay.**")
            return
        try:
            song = await player.toggle_song_loop()
        except:
            await ctx.send(f"<:error:805750300450357308> **Cannot loop music. No music is played.**")
            return
            
        if song.is_looping:
            await ctx.send(f":infinity: **Enabled loop for** `{song.name}`")
            
            
        else:
            await ctx.send(f":infinity: **Disabled loop for** `{song.name}`")
            
            
    @commands.command(aliases=['s'])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def shuffle(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        try:
            message = await ctx.send(":revolving_hearts: ** loading shuffle.**")
            player = music.get_player(guild_id=ctx.guild.id)
            liste_music = []
            cmpt=0
            for song in player.current_queue():
                if cmpt+1 == 1:
                    cmpt+=1
                    pass
                else:
                    liste_music.append(song.url)
                    song = await player.remove_from_queue(cmpt)
                    cmpt+=1
            random.shuffle(liste_music)
            for song in liste_music:
                song = await player.queue(song, search=False)
            
            await message.edit(content=":revolving_hearts: ** queue shuffle!**")
        except:
            await ctx.send(f"<:error:805750300450357308> **No music played**")
            
        
        
    @commands.command(aliases=['q'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def queue(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = music.get_player(guild_id=ctx.guild.id)
        name = []
        duration = []
        url = []
        
        if player is None:
            await ctx.send("<:error:805750300450357308> **Queue is empty.**")
            return
        
        for song in player.current_queue():
            name.append(song.name)
            duration.append(song.duration)
            url.append(song.url)
            
        embed = discord.Embed(color=embed_color(ctx.guild.id), title=f"Queue")
        embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
        
        embed.add_field(name="In progress", value=f"**[{name[0]}]({url[0]})** ` duration {convert_duration(duration[0])}`", inline=False)

        if len(name) >= 2:
            embed.add_field(name="Next", value=f"**[{name[1]}]({url[1]})** `duration {convert_duration(duration[1])}`", inline=False)
            cmpt=0
            text=" "
            if len(name) > 2:
                for i in name:
                    if cmpt >= 2:
                        text= text + f"[{name[cmpt]}]({url[cmpt]}) `Position: {cmpt}`, ` duration {convert_duration(duration[cmpt])}`\n\n"
                    cmpt+=1
                embed.add_field(name="After", value=f"{text}", inline=False)
           
        all_duration=0
        for i in duration:
            all_duration = all_duration+i

        embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/805066192834396210/813037403731918908/Songs.png",
                        text=f"{len(name)} song in Song'Queue. {convert_duration(all_duration)} total duration")
        
        await ctx.send(embed=embed)
    
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
        
        try:
            player = music.get_player(guild_id=ctx.guild.id)
            song = player.now_playing()
            try:
                pourcent = (playing_duration(ctx, int(song.duration))*100)/int(song.duration)
        
                barre="▬"*int((int(pourcent)/5))
                final=""
                error=0
                for i in list(range(20)):
                    try:
                        final=final+barre[i]
                    except:
                        if error == 0:
                            final=final+":nottub_oidar:"
                        else:
                            final=final+"▬"
                        error+=1     
                embed = discord.Embed(color=embed_color(ctx.guild.id), description=f"""**[{song.title}]({song.url})**\n`{convert_duration(playing_duration(ctx, song.duration))}/{convert_duration(song.duration)}`\n\n**|{"".join(reversed(final))}|**""")  
            except:
                embed = discord.Embed(color=embed_color(ctx.guild.id), description=f"""**[{song.title}]({song.url})**""")
            embed.set_author(name=f"Info", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=song.thumbnail)
            embed.add_field(name="Autor", value=f"{song.channel}", inline=True)        
            embed.add_field(name="Duration", value=f"{convert_duration(song.duration)}", inline=True)
            embed.add_field(name="views", value=f"{numerize.numerize(song.views)}", inline=True)
            embed.add_field(name="loop", value=f"{song.is_looping}", inline=True)
            embed.add_field(name="time", value=f"{convert_duration(playing_duration(ctx, song.duration))}", inline=True)
        
        
            embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/805066192834396210/813037403731918908/Songs.png",
                text=f"Song")
            await ctx.send(embed=embed)
        except:
            await ctx.send("<:error:805750300450357308> **No musique played.**")
            return
    
   
    
    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def skip(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            data = await player.skip(force=True)
        except:
            await ctx.send("<:error:805750300450357308> **No music playing.**")
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
            
        
        skipped=player.current_queue()
        if len(skipped) >= 2:
            skipped= player.current_queue()
            if value == "True":
                emoji = '\N{THUMBS UP SIGN}'
                await ctx.message.add_reaction(emoji)
            else:
                embed = discord.Embed(color=embed_color(ctx.guild.id), description=f"**:track_next: Skipped!**")
                try:
                    embed.set_thumbnail(url=skipped[1].thumbnail)
                except:
                    try:
                        embed.set_thumbnail(url=skipped[0].thumbnail)
                    except:
                        pass
                embed.add_field(name="Autor", value=f"{skipped[1].channel}", inline=True)       
                embed.add_field(name="Duration", value=f"{convert_duration(skipped[1].duration)}", inline=True)
                embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/805066192834396210/813037403731918908/Songs.png",
                            text=f"Song")
            
                await ctx.send(embed=embed)
        else:
            await ctx.send(f":track_next: **Skipped** `{data[0].name}`")

    @commands.command(aliases=['r'])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def remove(self, ctx, index):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.current_queue()
        try:
            song = await player.remove_from_queue(int(index))
        except:
            await ctx.send(f"<:error:805750300450357308> **Bad Index**\n`do remove [index] and index is an integer (position of the music in the queue)`")
            return
        await ctx.send(f":wastebasket: **Removed** `{song.name}` **from queue**")
        
        
    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def replay(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        if not ctx.author.voice:
            await ctx.send("<:error:805750300450357308> **You are not connected to a voice channel.**")
            return
        
        player = music.get_player(guild_id=ctx.guild.id)
        song=None
        
        try:
            song = player.now_playing()
        except:
            await ctx.send("<:error:805750300450357308> **No music playing.**")
            return
            
        if not song.is_looping:
            song = await player.toggle_song_loop()
            server_replay.append(ctx.guild.id)
        else:
            await ctx.send("<:error:805750300450357308> **You cannot replay music that has not been looped. Skip the song if necessary:** `skip`")
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
            
        if value == "True":
            await ctx.send(":rewind: Replay Song actived!")
        else:
            embed = discord.Embed(color=embed_color(ctx.guild.id), description=f"**[{song.title}]({song.url})**")     
            embed.set_author(name=f"Replay", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=song.thumbnail)
            embed.add_field(name="Autor", value=f"{song.channel}", inline=True)        
            embed.add_field(name="Duration", value=f"{convert_duration(song.duration)}", inline=True)
            embed.add_field(name="views", value=f"{numerize.numerize(song.views)}", inline=True)
            embed.add_field(name="loop", value=f"{song.is_looping}", inline=True)
        
            embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/805066192834396210/813037403731918908/Songs.png",
                text=f"Song")
           
            await ctx.send(embed=embed)
        await asyncio.sleep(song.duration)
       
        if song.is_looping:
            await player.toggle_song_loop()
           
            del server_replay[server_replay.index(ctx.guild.id)]
    
    
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            if member.id == 805082505320333383:
                player = music.get_player(guild_id=member.guild.id)
                if player != None:
                    await player.stop()
                    ctx=dict_ctx[member.guild.id]
                    
                    if ctx.voice_client is not None:
                        ctx.voice_client.cleanup()
        
    
    
        
def setup(client):
    client.add_cog(Play(client))