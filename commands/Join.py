from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
import DiscordUtils


class Join(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
            await ctx.send(":arrow_right: **Songs joined the voice channel.**")
            
        except:
            await ctx.send("<:error:805750300450357308> **You are not connected to a voice channel.**")
    

    
       
        
def setup(client):
    client.add_cog(Join(client))