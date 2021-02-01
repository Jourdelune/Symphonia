from utils.Constants import Constants
from utils.CreateTable import CreateTable
from discord.ext import tasks, commands
import datetime
import discord
from utils.utils import *
import os
  
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")

create_table = CreateTable()

try:
    posts = Utils.read_database('Bot', 'connexion')
except:
    write_database_for_one_value('Bot', 'connexion', f'{datetime.date.today()}0')

for filename in os.listdir('events'):
    if filename.endswith('.py'):
        bot.load_extension(f'events.{filename[:-3]}')

for filename in os.listdir('commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

            
bot.run(Constants.TOKEN)