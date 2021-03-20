import discord
from discord.ext import commands
from quart import Quart, redirect, url_for, render_template, g, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext.ipc import Server
import json

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ipc_ready(self):
        print("IPC ready")
    
    async def on_ready(self):
        print("Bot ready")
        
    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        print(endpoint, "raised", error)

bot = Bot(command_prefix="!", case_insensitive=True, help_command=None)
bot.remove_command("help")

bot_ipc = Server(bot, "127.0.0.1", "secret_key")



@bot_ipc.route() 
async def get_guild_count(data):
    return len(bot.guilds)

@bot_ipc.route() 
async def get_channel(data):
    channel = bot.get_channel(int(data.channel_id))
    return channel.name

@bot_ipc.route() 
async def get_all_channel(data):
    guild = bot.get_guild(int(data.guild_id))
    channel_list = []
    for channel in guild.text_channels:
        channel_list.append([channel.id, channel.name])

    with open('list.json', 'w') as json_file:
        json.dump(channel_list, json_file)
   

@bot_ipc.route() 
async def get_owner_with_id(data):
    guild = bot.get_guild(int(data.guild_id))
    return guild.owner_id

@bot_ipc.route() 
async def get_guild_list(data):
    list_id = []
    for i in bot.guilds:
        list_id.append(i.id)
        
    return list_id
        

if __name__ == "__main__":
    bot_ipc.start()
    bot.run("ODA1MDgyNTA1MzIwMzMzMzgz.YBVtgg.ie3BSi7q6z2SmEKSymLuA4mNj4Y")