from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
import DiscordUtils


class Leave(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
            await ctx.send(":arrow_left: **Songs left the voice channel.**")
        except:
            await ctx.send("<:error:805750300450357308> **The bot is not connected to a voice channel.**")
       
        
def setup(client):
    client.add_cog(Leave(client))