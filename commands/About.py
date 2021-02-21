from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
from utils.utils import *
from dateutil.relativedelta import relativedelta
from numerize import numerize
import psutil


class About(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.uptime1=time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        self.uptime1=time.time()
        
        
    @commands.command()
    async def about(self, ctx):
        """About cmd"""
        embed = discord.Embed(color=embed_color(), title="Song's Bot", description="Song's Bot is a music bot easy to use with a dashboard and a customizable behavior")
        embed.add_field(name="__Information:__", value=f"**<:arrowright:812991627424825364> Developer:** Jourdelune#8616\n**<:arrowright:812991627424825364> Library:** discord.py 1.6.0\n<:arrowright:812991627424825364> **Uptime:** {convert_duration(time.time()-self.uptime1)}", inline=False)
        embed.add_field(name="__Système:__", value=f"**<:arrowright:812991627424825364> CPU usage:** {psutil.cpu_percent()}%\n<:arrowright:812991627424825364> **RAM:** {round(psutil.virtual_memory().used / 1000000)}/{round(psutil.virtual_memory().total / 1000000)}mo\n<:arrowright:812991627424825364> **Ping:** {round(self.client.latency * 1000)}ms", inline=False)
        embed.add_field(name="__Bot:__", value=f"**<:arrowright:812991627424825364> Servers:** {str(len(list(self.client.guilds)))}\n<:arrowright:812991627424825364> **Users:** {len(list(self.client.get_all_members()))}\n<:arrowright:812991627424825364> **Shard:** {self.client.shard_count}", inline=False)
        await ctx.send(embed=embed)
            
       
        
def setup(client):
    client.add_cog(About(client))