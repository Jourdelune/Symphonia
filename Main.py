from discord.ext import commands, tasks
import os
from threading import Thread
import time
import re
import lavalink
import discord
from utils.Constants import Constants
from utils.CreateTable import CreateTable
import datetime
from utils.utils import *
import os

  
def get_prefix(client, message):
    data = str(read_database(table_name="config", data_in="prefix", data=f"WHERE guild_id={message.guild.id}"))
    if data != "None":
        prefix=str(read_database(table_name="config", data_in="prefix", data=f"WHERE guild_id={message.guild.id}"))
        return commands.when_mentioned_or(prefix)(client, message)
    else:
        try:
            write_in_database(table_name="config", data_in_name="guild_id", data_in=message.guild.id,
                                    data_for_write_name="prefix", data_for_write="s!")

            prefix=str(read_database(table_name="config", data_in="prefix",data=f"WHERE guild_id={message.guild.id}"))
            return commands.when_mentioned_or(prefix)(client, message)
        except:
            pass
        
class Bot: 
    def __init__(self, **kwargs):
        self.intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())        
        self.bot.remove_command("help")
        self.bot.lavalinkpass = "yourpass"
        self.bot.lavalinkport = 6952
      
        for filename in os.listdir('events'):
            if filename.endswith('.py'):
                self.bot.load_extension(f'events.{filename[:-3]}')

        for filename in os.listdir('commands'):
            if filename.endswith('.py'):
                self.bot.load_extension(f'commands.{filename[:-3]}')
        print("-------------------------------\nRunning Bot!")
        self.bot.run("ODA1MDgyNTA1MzIwMzMzMzgz.YBVtgg.ie3BSi7q6z2SmEKSymLuA4mNj4Y")
        
class init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("The bot is ready!")
        self.bot.add_cog(Music(self.bot))
Bot()