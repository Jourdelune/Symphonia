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
        


def setup(bot):
    bot.add_cog(OnGuildJoin(bot))