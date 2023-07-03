from discord import app_commands
from discord.ext import commands
from discord import Interaction

class ping(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None :
        self.bot = bot
    
    @app_commands.command(name='ping', description='Outputs latency with server in ms')
    async def ping(self, interaction : Interaction) -> None:
        await interaction.response.send_message(f':ping_pong: pong! {round(round(self.bot.latency, 4) * 1000)}ms')
    
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        ping(bot)
    )