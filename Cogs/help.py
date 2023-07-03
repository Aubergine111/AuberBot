from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Embed
import datetime
import pytz

class help(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None :
        self.bot = bot
        self.embed = Embed(title='Help?',
                           description='Command list for bot',
                           timestamp=datetime.datetime.now(pytz.timezone('UTC')),
                           color=0x0071FF)
        self.embed.set_author(name="AuberBot", icon_url=bot.user.display_avatar)
        self.embed.add_field(name='Ping', value='Outputs latency with server in ms', inline=False)
        self.embed.add_field(name='Help', value='Outputs this', inline=False)
        self.embed.add_field(name='Purge', value='Purge message in this channel', inline=False)
        self.embed.add_field(name='Guess', value='You guess the ILL levels. you should use List name without spaces at front and back of its name. the answer is not case sensitive.\n(ex : arcturus unnerfed instead of Arcturus)', inline=False)
        self.embed.add_field(name='Fetch', value='Search name you provided in database', inline=False)
    
    @app_commands.command(name='help')
    async def help(self, interaction : Interaction) -> None:
        self.embed.set_footer(text='sent by ' + interaction.user.name, icon_url=interaction.user.display_avatar)
        await interaction.response.send_message(embed = self.embed)
    
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        help(bot)
    )