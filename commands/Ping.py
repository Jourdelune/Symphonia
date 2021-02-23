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
        """Ping link"""
        await ctx.send(f":ping_pong: **Pong!** ```{round(self.client.latency * 1000)}ms```")
            
       
        
def setup(client):
    client.add_cog(Ping(client))