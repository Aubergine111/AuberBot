from discord import app_commands
from discord.ext import commands
from discord import Interaction
import asyncio

class purge(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None :
        self.bot = bot
    
    @app_commands.command(name='purge', description='Remove message in this channel.')
    # @app_commands.describe(count = "How many message will be deleted")
    async def purge_message(self, interaction : Interaction, count : int) -> None:
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You don't have permission to use this command!")
            return
        await interaction.response.defer()
        await interaction.channel.purge(limit = int(count) + 1)
        msg = await interaction.channel.send(f':broom: Purged {count} message!')
        await asyncio.sleep(2)
        await msg.delete()
    
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        purge(bot)
    )