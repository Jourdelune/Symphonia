from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
from utils.utils import * 

class Vote(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def vote(self, ctx):
        """Vote link"""
        embed = discord.Embed(color=embed_color(), description="[top.gg link](https://top.gg)")
        embed.set_author(name=f"Vote song's Bot", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
            
       
        
def setup(client):
    client.add_cog(Vote(client))