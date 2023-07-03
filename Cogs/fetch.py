from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Embed
import discord
import datetime
import pytz
import sqlite3
import asyncio

class fetch(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None :
        self.bot = bot
        self.diffList = ['None', 'Easy', 'Normal', 'Hard', 'Impossible']
    
    @app_commands.command(name='fetch', description="Find level with it's name.")
    @app_commands.describe(levelname = "Level\'s name")
    async def fetch(self, interaction : Interaction, levelname : str) -> None:
        self.embed = Embed(timestamp=datetime.datetime.now(pytz.timezone('UTC')),
                           color=0x0071FF)
        self.embed.set_author(name="AuberBot", icon_url=self.bot.user.display_avatar)
        self.SQLConnection = sqlite3.connect('./test.db', isolation_level=None)
        cur = self.SQLConnection.cursor()
        cur.execute('select * from levels where LOWER(levelName) = ?', (levelname.lower(), ))
        rows = cur.fetchall()
        rowcount = len(rows)
        if rowcount < 1 :
            await interaction.response.send_message('There is no level with that name!')
            return
        rowlist = []
        for row in rows:
            rowlist.append(row)
        
        await interaction.response.send_message(embed = self.embed)
        msg = await interaction.original_response()
        emojis = ['⬅️','➡️']
        
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
        
        rownum = 0
        
        while True:
            try:
                row = rowlist[rownum]
                print(row)
                self.embed.title = row[1]
                self.embed.description = 'Difficulty : ' + self.diffList[row[3]] + f' | Internal ID : {row[0]}'
                self.embed.set_image(url=row[2])
                self.embed.set_footer(text='sent by ' + interaction.user.name + f' | Page {rownum + 1} / {rowcount}', icon_url=interaction.user.display_avatar)
                await interaction.edit_original_response(embed = self.embed)  
                await interaction.client.wait_for("reaction_add", check = check, timeout = 15)
                
                if self.rct.emoji == '⬅️' and rownum > 1:
                    rownum -= 1
                elif self.rct.emoji == '➡️' and rownum < rowcount - 1:
                    rownum += 1
                await self.rct.remove(self.user)
            except asyncio.TimeoutError:
                break
        
        await msg.remove_reaction('⬅️', self.bot.user)
        await msg.remove_reaction('➡️', self.bot.user)
        
        self.SQLConnection.close()
    #i need to finish this someday ngl

    # @app_commands.command(name='fetch', description="Find level with it's internal ID")
    # @app_commands.describe(levelID = "Internal ID of the level")
    # async def fetch(self, interaction : Interaction, levelID : int) -> None:
    #     self.embed = Embed(timestamp=datetime.datetime.now(pytz.timezone('UTC')),
    #                        color=0x0071FF)
    #     self.embed.set_author(name="AuberBot", icon_url=self.bot.user.display_avatar)
    #     self.SQLConnection = sqlite3.connect('./test.db', isolation_level=None)
    #     cur = self.SQLConnection.cursor()
    #     cur.execute('select * from levels where levelID = ?', (levelID, ))
    #     row = cur.fetchone()
    #     if not row :
    #         await interaction.response.send_message('There is no level with that ID!')
    #         return
    #     print(row)
    #     self.embed.title = row[1]
    #     self.embed.description = 'Internal ID : ' + str(levelID) + ' | Difficulty : ' + self.diffList[row[3]]
    #     self.embed.set_image(url=row[2])
    #     self.embed.set_footer(text='sent by ' + interaction.user.name, icon_url=interaction.user.display_avatar)
    #     await interaction.response.send_message(embed = self.embed)
    #     self.SQLConnection.close()
    
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        fetch(bot)
    )
