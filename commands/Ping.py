from discord.ext import commands
import discord
import asyncio
import time
import asyncio
from utils.utils import * 
import psutil

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def ping(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)

  
            return
        
        """Ping link"""
        await ctx.send(f":ping_pong: **Pong!** ```{round(self.client.latency * 1000)}ms```")
            
       
        
def setup(client):
    client.add_cog(Ping(client))