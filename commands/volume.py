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
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))
       
        
def setup(client):
    client.add_cog(Volume(client))