from discord.ext import tasks, commands
import discord
import asyncio
import utils
import time
import asyncio
from utils.utils import *
from dateutil.relativedelta import relativedelta
from numerize import numerize
import psutil

list_user=[]

class About(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.uptime1=time.time()
        self.compteur = 0
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.uptime1=time.time()
        
         

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.compteur+=1
        if (ctx.author.id not in list_user):
            list_user.append(ctx.author.id)
        
    @tasks.loop(seconds=3600)
    async def check_time(self):
        self.compteur=0
        
    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def about(self, ctx):
        verif_channel=get_channel(ctx.guild.id, ctx.channel.id)
        if verif_channel == True:
            pass
        else:
            embed = discord.Embed(color=discord.Colour.red(), title="<:error:805750300450357308> Error", description=f"You cannot make commands in this channel. Go to this one: <#{verif_channel}>")
            await ctx.send(embed=embed, delete_after=3.0)

            await ctx.send(embed=embed, delete_after=3.0)
            return
        
        """About cmd"""
        embed = discord.Embed(color=embed_color(ctx.guild.id), title="Song's Bot", description="Song's Bot is a music bot easy to use with a dashboard and a customizable behavior")
        embed.add_field(name="__Information:__", value=f"**<:arrowright:812991627424825364> Developer:** Jourdelune#8616\n**<:arrowright:812991627424825364> Library:** discord.py 1.6.0\n<:arrowright:812991627424825364> **Uptime:** {convert_duration(time.time()-self.uptime1)}", inline=False)
        embed.add_field(name="__System:__", value=f"**<:arrowright:812991627424825364> CPU usage:** {psutil.cpu_percent()}%\n<:arrowright:812991627424825364> **RAM:** {round(psutil.virtual_memory().used / 1000000)}/{round(psutil.virtual_memory().total / 1000000)}mo\n<:arrowright:812991627424825364> **Ping:** {round(self.client.latency * 1000)}ms", inline=False)
        embed.add_field(name="__Bot:__", value=f"**<:arrowright:812991627424825364> Servers:** {str(len(list(self.client.guilds)))}\n<:arrowright:812991627424825364> **Users:** {len(list(self.client.get_all_members()))}\n<:arrowright:812991627424825364> **Shard:** {self.client.shard_count}", inline=False)
        embed.add_field(name="__Statistic:__", value=f"**<:arrowright:812991627424825364> Command hours:** {self.compteur}\n<:arrowright:812991627424825364> **Really user after uptime:** {len(list_user)}", inline=False)
        embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/805082505320333383/f0b2ffbe37e3eaae7bd23ec02d666bf1.png?size=256",
                             text=f"Powered by flo-x.fr")
        await ctx.send(embed=embed)
            
       
        
def setup(client):
    client.add_cog(About(client))