
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Embed
import datetime
import pytz
import sqlite3
import asyncio
import discord

class insert(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None :
        self.bot = bot
    
    @app_commands.command(name='insert', description="add level to bot's database.")
    @app_commands.describe(levelname = "Level\'s name", imglnk = 'link of the image of level', diff = 'difficulty')
    @app_commands.choices(diff = [
        app_commands.Choice(name = 'Easy', value = 1),
        app_commands.Choice(name = 'Normal', value = 2),
        app_commands.Choice(name = 'Hard', value = 3),
        app_commands.Choice(name = 'Impossible', value = 4)
    ])
    async def insert(self, interaction : Interaction, levelname : str, imglnk : str, diff : app_commands.Choice[int]) -> None:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to use this command!")
            return
        self.embed = Embed(timestamp=datetime.datetime.now(pytz.timezone('UTC')),
                           color=0x0071FF)
        self.embed.set_author(name="AuberBot", icon_url=self.bot.user.display_avatar)
        self.SQLConnection = sqlite3.connect('./test.db', isolation_level=None)
        cur = self.SQLConnection.cursor()
        
        await interaction.response.send_message("Wait for a moment...")
        
        
        cur.execute('select * from levels where LOWER(levelName) = ?', (levelname.lower(), ))
        row = cur.fetchone()
        if row :
            await interaction.edit_original_response(content='There is a level with this name already. are you really trying to add this level with this name?')
            
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
            
                if self.rct.emoji == '❌':
                    await msg.reply('Action canceled!')
                    await msg.remove_reaction('✔️', self.bot.user)
                    await msg.remove_reaction('❌', self.bot.user)
                    return
                    
                await self.rct.remove(self.user)
                await msg.remove_reaction('✔️', self.bot.user)
                await msg.remove_reaction('❌', self.bot.user)
            except asyncio.TimeoutError:
                await msg.reply('You didn\'t responded for 30 second so action was canceled!')
                await msg.remove_reaction('✔️', self.bot.user)
                await msg.remove_reaction('❌', self.bot.user)
                return
        
        cur.execute("INSERT INTO levels (levelID, levelName, imgLnk, diff) VALUES((select ifnull(max(l.levelID), 0) from levels l) + 1, ?, ?, ?);", (levelname, imglnk, diff.value))
        cur.execute('select * from levels where levelID = (select ifnull(max(l.levelID), 0) from levels l)')
        row = cur.fetchone()
        print(row)
        self.embed.title = levelname + ' inserted to database'
        self.embed.description = f'Level inserted to database with this image. Internal ID : {row[0]}'
        self.embed.set_image(url=imglnk)
        self.embed.set_footer(text='sent by ' + interaction.user.name, icon_url=interaction.user.display_avatar)
        await interaction.edit_original_response(content = ' ', embed = self.embed)
        self.SQLConnection.close()
    
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        insert(bot)
    )