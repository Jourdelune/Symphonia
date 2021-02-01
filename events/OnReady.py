from discord.ext import commands
import discord


class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as {0} ({0.id})'.format(self.client.user))
        print('------')
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name="songs Bot | !help"))

         

def setup(client):
    client.add_cog(OnReady(client))