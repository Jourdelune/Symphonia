from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
from utils.utils import * 

class Support(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def support(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)

            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        """Support link"""
        embed = discord.Embed(color=embed_color(ctx.guild.id), description="[support link](https://discord.gg/qaQtvNmdm5)")
        embed.set_author(name=f"Support of song's Bot", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
            
       
        
def setup(client):
    client.add_cog(Support(client))