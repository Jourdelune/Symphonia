from discord.ext import commands
from utils.utils import *
import discord

class OnGuildJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(818588133855068240)
 
        embed = discord.Embed(color=embed_color(guild.id), title="Delete Guild", description=f"`{guild.owner.name}` delete Song on `{guild.name}`.")
        await channel.send(embed=embed)
        
        
    
        
                
                
            
        
        
        
        


def setup(bot):
    bot.add_cog(OnGuildJoin(bot))