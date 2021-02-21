from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
from utils.utils import * 

class Support(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def support(self, ctx):
        """Support link"""
        embed = discord.Embed(color=embed_color(), description="[support link](https://discord.gg/qaQtvNmdm5)")
        embed.set_author(name=f"Support of song's Bot", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
            
       
        
def setup(client):
    client.add_cog(Support(client))