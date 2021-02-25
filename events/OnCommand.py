from discord.ext import tasks, commands
from utils.utils import *
import discord
import psutil
import sys
import subprocess
import os

class OnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if "cooldown" in str(error):
            embed = discord.Embed(color=discord.Colour.red(), title=":alarm_clock: Cooldown", description=f"**{str(error)}**")
            await ctx.send(embed=embed, delete_after=3.0)
            return
            
        if "You are missing Manage Channels permission(s) to run this command." in str(error):
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You are missing Manage Channels permission(s) to run this command. `Manage Channels`")
            await ctx.send(embed=embed, delete_after=3.0)
            return
            
        if "required argument that is missing." in str(error):
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"{error}")
            await ctx.send(embed=embed, delete_after=3.0)
            return
            
        else:
            channel = self.bot.get_channel(805066193047519236)
            try:
                raise error
                await channel.send(f'Error on {ctx.guild.name}: ```{error}```')
            except:
                raise error
                
               
                
            
        
            
    


def setup(bot):
    bot.add_cog(OnCommand(bot))