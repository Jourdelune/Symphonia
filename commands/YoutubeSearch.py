import asyncio
from discord.ext import commands
import discord
from utils.utils import * 
from youtubesearchpython import *



class YoutbeSearchTo(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def search(self, ctx, *, url=""):
        """YoutbeSearch link"""
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        if url == "":
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You must specify what you are looking for.")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        if len(url) >= 200:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"Your search must not exceed 200 characters.")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        message = await ctx.send(f"<:search:805751542920773633> **currently researching** `{url}`.")
        search = VideosSearch(url, limit = 10)

        
        embed = discord.Embed(color=embed_color(ctx.guild.id), title=f"Search Result")
    
       

        for i in search.result()['result']:
            embed.add_field(name=f"{i['title']}", value=f"{i['link']}", inline=False)
        embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
        
        await message.edit(content=None, embed=embed)
  
            
       
        
def setup(client):
    client.add_cog(YoutbeSearchTo(client))