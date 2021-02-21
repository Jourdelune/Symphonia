from discord.ext import tasks, commands
from utils.utils import *
import discord

class OnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if "cooldown" in str(error):
            embed = discord.Embed(color=discord.Colour.red(), title=":bell: Cooldown", description=f"**{str(error)}**")
            await ctx.send(embed=embed)
            
    


def setup(bot):
    bot.add_cog(OnCommand(bot))