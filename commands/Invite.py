from discord.ext import commands
import discord
import asyncio
import utils
import time
import asyncio
from utils.utils import * 

class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['i'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def invite(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        """Invite link"""
        embed = discord.Embed(color=embed_color(ctx.guild.id), description="[link song's Bot](https://discord.com/oauth2/authorize?client_id=805082505320333383&scope=bot&permissions=70634560)")
        embed.set_author(name=f"Invite song's Bot", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
            
       
        
def setup(client):
    client.add_cog(Invite(client))