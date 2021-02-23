from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
from utils.utils import * 

class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def invite(self, ctx):
        """Invite link"""
        embed = discord.Embed(color=embed_color(), description="[link song's Bot](https://discord.com/oauth2/authorize?client_id=805082505320333383&scope=bot&permissions=70634560)")
        embed.set_author(name=f"Invite song's Bot", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
            
       
        
def setup(client):
    client.add_cog(Invite(client))