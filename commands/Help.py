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
**[Dashboard link](https://lol)\n[Documentation link](https://lol2)\n[Vote link](https://lol2)\n[Bot invite](https://lol2)\n\n**""")
        embed.add_field(name="**:notes: Music**", value=f"`play` `replay` `skip` `stop` `pause` `resume` `loop` `queue` `volume` `np` `leave` `join` `remove` `shuffle`\n\n", inline=False)
        embed.add_field(name="**:computer: Song's Bot**", value=f"`invite` `about` `support` `vote` `ping` `help`\n\n", inline=False)
        embed.add_field(name="**:tools: Gestion**", value=f"**[Go to Dashboard](https://lol)**\n", inline=False)
        embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/805082505320333383/f0b2ffbe37e3eaae7bd23ec02d666bf1.png?size=256",
                             text=f"Do help [command] for more info on a command.")
            
        await ctx.send(embed=embed)
        
       
        
def setup(client):
    client.add_cog(Volume(client))