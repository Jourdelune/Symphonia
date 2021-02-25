from discord.ext import commands
from utils.utils import *
import discord

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(f'<@!805082505320333383>'):
            prefix="None"
            data = str(read_database(table_name="config", data_in="prefix", data=f"WHERE guild_id={message.guild.id}"))
            if data != "None":
                prefix = str(read_database(table_name="config", data_in="prefix", data=f"WHERE guild_id={message.guild.id}"))
            else:
                try:
                    write_in_database(table_name="config", data_in_name="guild_id", data_in=message.guild.id,
                                    data_for_write_name="prefix", data_for_write="s!")

                    prefix = str(read_database(table_name="config", data_in="prefix",data=f"WHERE guild_id={message.guild.id}"))
                except:
                    prefix = "s!"
                
            embed = discord.Embed(color=embed_color(message.guild.id), title=f"Hi {message.author.name}", description=f"My Prefix on this guild is {prefix}.")
            await message.channel.send(embed=embed)
        


def setup(bot):
    bot.add_cog(OnMessage(bot))