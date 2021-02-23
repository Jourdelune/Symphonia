import discord
from discord.ext import commands
from quart import Quart, redirect, url_for, render_template, g, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext.ipc import Server

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ipc_ready(self):
        print("IPC ready")
    
    async def on_ready(self):
        print("Bot ready")

bot = Bot(command_prefix="!", case_insensitive=True)
bot_ipc = Server(bot, "localhost", 8765, "secret_key")



@bot_ipc.route() 
async def get_guild_count(data):
    return len(bot.guilds)

@bot_ipc.route() 
async def get_owner_with_id(data):
    guild = bot.get_guild(int(data.guild_id))
    print(guild.owner_id)
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