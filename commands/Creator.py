from discord.ext import commands
import discord
import asyncio
import time
import asyncio
from utils.utils import * 
import psutil
import sys
import subprocess
import os

class Creator(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def reboot(self, ctx):
        if ctx.author.id == 640518207257444374:
            await ctx.send("reboot")
            await ctx.bot.logout()
            subprocess.call([sys.executable, "Main.py"])
      
   
        
    @commands.command()
    async def reload(self, ctx, cog=None):
        if ctx.author.id == 640518207257444374:
            if cog == None:
                await ctx.send("please enter a cog")
                return
            
            cog1 = cog + ".py"
            cog1 = cog + ".py"
            if cog1 in os.listdir('commands'):
                folder = "commands"
            else:
                if cog1 in os.listdir('events'):
                    folder = "events"
                else:
                    await ctx.send("no cogs founded")
                    return
    
            ctx.bot.reload_extension(folder + "." + cog)
            await ctx.send(f"{folder}.{cog} reload!")
        
def setup(client):
    client.add_cog(Creator(client))