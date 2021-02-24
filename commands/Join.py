from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
import DiscordUtils
from utils.utils import *
import sys

class Join(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['j'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def join(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)

            return
        
        try:
            await ctx.author.voice.channel.connect()
            await ctx.send(":arrow_right: **Songs joined the voice channel.**")
            
        except:
            if ctx.author.voice:
                await ctx.send("<:error:805750300450357308> **Already connected to the voice.**")
            else:
                await ctx.send("<:error:805750300450357308> **You are not connected to a voice channel.**")
    

    
       
        
def setup(client):
    client.add_cog(Join(client))