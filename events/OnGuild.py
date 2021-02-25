from discord.ext import commands
from utils.utils import *
import discord

class OnGuildJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(805066193047519237)
 
        embed = discord.Embed(color=embed_color(guild.id), title="New Guild", description=f"`{guild.owner.name}` added Song on `{guild.name}`.")
        await channel.send(embed=embed)
        
        
        if guild.system_channel is not None:
            embed = discord.Embed(color=embed_color(guild.id), title="Song - A music bot that's easy to use!", description=f"Thanks for adding Song Bot\n\nIf you want to play music, perform `s!play`.\nFor help, perform the following steps `s!help`.\nTo configure the bot, go to the [dashboard](https://songs-bot.tk/me).\n\nYou can also join the [support server](https://discord.gg/qaQtvNmdm5) to receive help.\nOnce again, thank you for choosing Song Bot and good music.")
            await guild.system_channel.send(embed=embed)
        
                
                
            
        
        
        
        


def setup(bot):
    bot.add_cog(OnGuildJoin(bot))