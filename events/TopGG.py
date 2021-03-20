from discord.ext import commands, tasks
import discord
import dbl


class TopGG(commands.Cog):
    """
    This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 30 minutes.
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgwNTA4MjUwNTMyMDMzMzM4MyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE1NzA0NjA1fQ.srX61MkOVRsjAgF2_4yVGwHLC7RJINCZQJike33Noh8'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        await self.bot.wait_until_ready()
        try:
            server_count = len(list(self.bot.guilds))
            await self.dblpy.post_guild_count(server_count)
            print('Posted server count ({})'.format(server_count))
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))


def setup(bot):
    bot.add_cog(TopGG(bot))