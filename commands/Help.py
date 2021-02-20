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


    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(color=embed_color(), title="Song's Bot help page", description=f"""Song's Bot is a music bot **easy to use** with **a dashboard** and **a customizable behavior**.\n
Song's Bot is a music bot **easy to use** with a dashboard and a customizable behavior** \n\n[Dashboard link](https://lol)\n[Documentation link](https://lol2)\n[Vote link](https://lol2)**""")
       
        embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/805082505320333383/f0b2ffbe37e3eaae7bd23ec02d666bf1.png?size=256",
                             text=f"Song'Bot help page")
            
        await ctx.send(embed=embed)
        
       
        
def setup(client):
    client.add_cog(Volume(client))