from discord.ext import tasks, commands
import asyncio
import discord
from utils.utils import *
import re
import discord
from dateutil.relativedelta import relativedelta
import DiscordUtils

music = DiscordUtils.Music()

class Play(commands.Cog):
    def __init__(self, client):
        self.bot = client
        
    @commands.command()
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
            await ctx.send(":arrow_right: **Songs joined the voice channel.**")
        except:
            await ctx.send("<:error:805750300450357308> **You are not connected to a voice channel.**")
    
    @commands.command()
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
            await ctx.send(":arrow_left: **Songs left the voice channel.**")
        except:
            await ctx.send("<:error:805750300450357308> **The bot is not connected to a voice channel.**")
    
    @commands.command()
    async def play(self, ctx, *, url):
        if not ctx.author.voice:
            return
        
        message = await ctx.send(f"<:search:805751542920773633> **currently researching** `{url}`.")
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            try:
                await player.queue(url, search=True)
            except:
                try:
                    await player.queue(url, bettersearch=True)
                except:
                    await ctx.send(f"<:error:805750300450357308> **An error has occurred. Put a correct search.**")
                    return
            song = await player.play()
            embed = discord.Embed(color=embed_color(), description=f"**[{song.title}]({song.url})**")
            embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=song.thumbnail)
            embed.add_field(name="Autor", value=f"{song.channel}", inline=True)
            duration=relativedelta(seconds=round(float(song.duration)))
            if duration.hours != 0:
                duration=str(duration.hours)+":"+str(duration.minutes)+":"+str(duration.seconds)
            else:
                duration=str(duration.minutes)+":"+str(duration.seconds)
                
            embed.add_field(name="Duration", value=f"{duration}", inline=True)
            embed.add_field(name="Estimated time until playing", value=f"0", inline=True)
            embed.add_field(name="position", value=f"0", inline=True)
            embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/805082505320333383/ee1b4512c41ca4d2d70cefb7342bbbc6.png?size=256",
                             text=f"Song")
            
            await message.edit(content=None, embed=embed)

        else:
            try:
                song = await player.queue(url, search=True)
                embed = discord.Embed(color=embed_color(), description=f"**[{song.title}]({song.url})**")     
                embed.set_author(name=f"Added to queue", icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=song.thumbnail)
                embed.add_field(name="Autor", value=f"{song.channel}", inline=True)
                duration=relativedelta(seconds=round(float(song.duration)))
                if duration.hours != 0:
                    duration=str(duration.hours)+":"+str(duration.minutes)+":"+str(duration.seconds)
                else:
                    duration=str(duration.minutes)+":"+str(duration.seconds)
                
                player = music.get_player(guild_id=ctx.guild.id)
                all_duration=0
                position=0
                for i in player.current_queue():
                    if song.url != i.url:
                        all_duration=all_duration+i.duration
                        position+=1
                    else:
                        break

                embed.add_field(name="Duration", value=f"{duration}", inline=True)
                embed.add_field(name="time until playing", value=f"{convert_duration(all_duration+song.duration)}", inline=True)
                embed.add_field(name="position", value=f"{position}", inline=True)
                embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/805082505320333383/ee1b4512c41ca4d2d70cefb7342bbbc6.png?size=256",
                             text=f"Song")
      
                await message.edit(content=None, embed=embed)
            except:
                await ctx.send(f"<:error:805750300450357308> **An error has occurred. Put a correct search.**")
                return
    
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("<:error:805750300450357308> **You are not connected to a voice channel.**")
 
    @commands.command()
    async def pause(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            song = await player.pause()
            await ctx.send(f"<:pause:805844063164039168> **Paused** `{song.name}`")
        except:
            await ctx.send(f"<:error:805750300450357308> **No music played**")
    
    @commands.command()
    async def resume(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            song = await player.resume()
            await ctx.send(f"<:play:805845139830472714> **Resumed** `{song.name}`")
        except:
            await ctx.send(f"<:error:805750300450357308> **No music played**")

    
    @commands.command()
    async def loop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            song = await player.toggle_song_loop()
        except:
            await ctx.send(f"<:error:805750300450357308> **Cannot loop music. No music is played.**")
            return
            
        if song.is_looping:
            await ctx.send(f"<:boucle:805907893714681947> **Enabled loop for** `{song.name}`")
        else:
            await ctx.send(f"<:stop_infinis:805908993284243516> **Disabled loop for** `{song.name}`")
    
    @commands.command()
    async def queue(self, ctx):       
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
            
        embed = discord.Embed(color=embed_color(), title=f"Queue")
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

        embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/805082505320333383/ee1b4512c41ca4d2d70cefb7342bbbc6.png?size=256",
                        text=f"{len(name)} song in Song'Queue. {convert_duration(all_duration)} total duration")
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def np(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await ctx.send(song.name)
    
    @commands.command()
    async def skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            data = await player.skip(force=True)
        except:
            await ctx.send("<:error:805750300450357308> **No music playing.**")
            return
        
        skipped=player.current_queue()
        if len(skipped) >= 2:
            skipped= player.current_queue()
        
            embed = discord.Embed(color=embed_color(), description=f"**:track_next: Skipped!**")
            embed.set_thumbnail(url=skipped[1].thumbnail)
            embed.add_field(name="Autor", value=f"{skipped[1].channel}", inline=True)       
            embed.add_field(name="Duration", value=f"{convert_duration(skipped[1].duration)}", inline=True)
            embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/805082505320333383/ee1b4512c41ca4d2d70cefb7342bbbc6.png?size=256",
                            text=f"Song")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(f":track_next: **Skipped** `{data[0].name}`")

    
    @commands.command()
    async def remove(self, ctx, index):
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            song = await player.remove_from_queue(int(index))
        except:
            await ctx.send(f"<:error:805750300450357308> **Bad Index**\n`do remove [index] and index is an integer (position of the music in the queue)`")
            return
        await ctx.send(f":wastebasket: **Removed** `{song.name}` **from queue**")
      
  
            
    

        
def setup(client):
    client.add_cog(Play(client))