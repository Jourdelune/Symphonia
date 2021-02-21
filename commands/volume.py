from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio


class Volume(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def volume(self, ctx, volume: int):
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