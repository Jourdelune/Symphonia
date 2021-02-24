from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
from utils.utils import * 

class Volume(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['h'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def help(self, ctx, *, arg=None):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
            
        
        if arg == None:
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Song's Bot help page", description=f"""Song's Bot is a music bot **easy to use** with **a dashboard** and **a customizable behavior**.\n
            **[Dashboard link](http://songs-bot.tk/me)\n[Documentation link](http://songs-bot.tk/commands)\n[Vote link](https://top.gg)\n[Bot invite](https://discord.com/oauth2/authorize?client_id=805082505320333383&scope=bot&permissions=70634560)\n\n**""")
            embed.add_field(name="**:notes: Music**", value=f"`play` `replay` `skip` `stop` `pause` `resume` `loop` `queue` `volume` `np` `leave` `join` `remove` `shuffle`\n\n", inline=False)
            embed.add_field(name="**:computer: Song's Bot**", value=f"`invite` `about` `support` `vote` `ping` `help`\n\n", inline=False)
            embed.add_field(name="**:tools: Gestion**", value=f"**[Go to Dashboard](https://lol)**\n", inline=False)
            embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/805082505320333383/f0b2ffbe37e3eaae7bd23ec02d666bf1.png?size=256",
                                 text=f"Do help [command] for more info on a command.")
        elif arg == "play":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="play [music]", description=f"Plays the desired music or adds it to the queue.")
            
        elif arg == "replay":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="replay", description=f"Re-launch the music currently in progress.")
            
        elif arg == "skip":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="skip", description=f"Skip to next music.")
            
        elif arg == "stop":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="stop", description=f"Stop the music and reset the tail.")
            
        elif arg == "pause":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="pause", description=f"Pauses music in progress.")
            
        elif arg == "resume":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Resume", description=f"Launches the music that was paused.")
            
        elif arg == "loop":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Loop", description=f"Plays the music in a loop or turns it off if necessary.")
            
        elif arg == "queue":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Queue", description=f"Displays the music queue.")
            
        elif arg == "volume":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Volume [0 at 100%]", description=f"Changes the volume of the music.")
            
        elif arg == "np":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="np", description=f"Displays information about the current music.")
            
        elif arg == "leave":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Leave", description=f"Leave the channel.")
            
        elif arg == "join":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Join", description=f"Join the channel.")
            
        elif arg == "remove":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Remove [position]", description=f"Removes music from the list via its position in its queue.")
            
        elif arg == "shuffle":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Shuffle", description=f"Randomly arrange the music.")
            
        elif arg == "invite":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Invite", description=f"Returns the bot's invitation link.")
            
        elif arg == "about":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="About", description=f"Returns information about the bot.")
            
        elif arg == "support":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Support", description=f"Returns the official discord support server.")
            
        elif arg == "vote":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Vote", description=f"Returns the link to vote on top.gg.")
            
        elif arg == "ping":
            embed = discord.Embed(color=embed_color(ctx.guild.id), title="Ping", description=f"Returns the ping of the bot.")
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"**No help found matching at `{arg}`**")
         
            
            
        await ctx.send(embed=embed)
        
       
        
def setup(client):
    client.add_cog(Volume(client))