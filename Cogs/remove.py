from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Embed
import discord
import datetime
import pytz
import sqlite3
import asyncio

class remove(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None :
        self.bot = bot
    
    @app_commands.command(name='remove', description="Remove level from bot's database")
    @app_commands.describe(levelid = "Level\'s ID")
    async def remove(self, interaction : Interaction, levelid : int) -> None:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to use this command!")
            return
        self.embed = Embed(timestamp=datetime.datetime.now(pytz.timezone('UTC')),
                           color=0x0071FF)
        self.embed.set_author(name="AuberBot", icon_url=self.bot.user.display_avatar)
        self.SQLConnection = sqlite3.connect('./test.db', isolation_level=None)
        cur = self.SQLConnection.cursor()
        cur.execute('select * from levels where levelID = ?', (levelid, ))
        row = cur.fetchone()
        if not row :
            await interaction.response.send_message('There is no level with that ID!')
            return
        self.embed.title = 'Are you really trying to remove ' + row[1] + ' from database?'
        self.embed.set_image(url=row[2])
        self.embed.set_footer(text='sent by ' + interaction.user.name, icon_url=interaction.user.display_avatar)
        await interaction.response.send_message(embed = self.embed)
        
        msg = await interaction.original_response()
        emojis = ['✔️', '❌']
        
        for emoji in emojis:
            await msg.add_reaction(emoji)
        self.rct = discord.Reaction
        self.user = discord.Member
            
        def check(reaction : discord.Reaction, user : discord.Member):
            if reaction.emoji not in emojis : return False
            if reaction.message.id != msg.id : return False
            if user.id != interaction.user.id : return False
            self.rct = reaction
            self.user = user
            return True
        
        try:
            await interaction.client.wait_for("reaction_add", check = check, timeout = 30)
        
            if self.rct.emoji == '✔️':
                
                cur.execute('delete from levels where levelID = ?', (row[0], ))
                self.embed.title = row[1] + ' removed from database'
                self.embed.description = 'Level successfully removed from database.'
                await interaction.edit_original_response(embed = self.embed)
            else:
                await msg.reply('Action canceled!')
                
            await self.rct.remove(self.user)
        except asyncio.TimeoutError:
            await msg.reply('You didn\'t responded for 30 second so action was canceled!')
        await msg.remove_reaction('✔️', self.bot.user)
        await msg.remove_reaction('❌', self.bot.user)
        self.SQLConnection.close()
    
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        remove(bot)
    )