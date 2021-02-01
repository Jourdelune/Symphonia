from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
import DiscordUtils
music = DiscordUtils.Music()

class Stop(commands.Cog):
    def __init__(self, client):
        self.client = client


    
       
        
def setup(client):
    client.add_cog(Stop(client))