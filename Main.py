from utils.Constants import Constants
from utils.CreateTable import CreateTable
from discord.ext import tasks, commands
import datetime
import discord
from utils.utils import *
import os
  
  
def get_prefix(client, message):
    data = str(read_database(table_name="config", data_in="prefix", data=f"WHERE guild_id={message.guild.id}"))
    if data != "None":
        return str(
            read_database(table_name="config", data_in="prefix", data=f"WHERE guild_id={message.guild.id}"))
    else:
        try:
            write_in_database(table_name="config", data_in_name="guild_id", data_in=message.guild.id,
                                    data_for_write_name="prefix", data_for_write="s!")

            return str(read_database(table_name="config", data_in="prefix",
                                           data=f"WHERE guild_id={message.guild.id}"))
        except:
            pass
            
bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
bot.remove_command("help")

create_table = CreateTable()

try:
    posts = read_database('Bot', 'connexion')
except:
    write_database_for_one_value('Bot', 'connexion', f'{datetime.date.today()}0')

for filename in os.listdir('events'):
    if filename.endswith('.py'):
        bot.load_extension(f'events.{filename[:-3]}')

for filename in os.listdir('commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

            
bot.run(Constants.TOKEN)