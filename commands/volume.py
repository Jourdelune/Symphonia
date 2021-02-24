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


    @commands.command(aliases=['v'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def volume(self, ctx, volume: int):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)

            return
        
        """Changes the player's volume"""

        if ctx.voice_client is None:
            await ctx.send("<:error:805750300450357308> **You are not connected to a voice channel.**")
            return

        ctx.voice_client.source.volume = volume / 100
        if volume == 0:
            await ctx.send(":mute: **Changed volume to {}%**".format(volume))
        else:
            await ctx.send(":loud_sound: **Changed volume to {}%**".format(volume))
            
       
        
def setup(client):
    client.add_cog(Volume(client))