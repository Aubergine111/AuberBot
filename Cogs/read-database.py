from discord import app_commands
from discord.ext import commands
from discord import Interaction, Embed
import discord
import datetime
import pytz
import sqlite3
import asyncio

class read_database(commands.Cog):
    difflist = []
    perpage = 20
    def __init__(self, bot:commands.Bot) -> None :
        self.bot = bot
        self.diffList = ['None', 'Easy', 'Normal', 'Hard', 'Impossible']
    
    @app_commands.command(name='list', description='List of the levels in this bot.')
    async def read_database(self, interaction : Interaction) -> None:
        self.felid = 1
        self.lelid = self.perpage
        # ⬅️ = 1
        # ➡️ = 1
        self.embed = Embed(title='List of levels in Database',
                           timestamp=datetime.datetime.now(pytz.timezone('UTC')),
                           color=0x0071FF)
        self.embed.set_author(name="AuberBot", icon_url=self.bot.user.display_avatar)
        self.SQLConnection = sqlite3.connect('./test.db', isolation_level=None)
        cur = self.SQLConnection.cursor()
        cur.execute('select * from levels')
        rows = cur.fetchall()
        rowcount = len(rows)
        pgcount = (int)((rowcount - 1) / self.perpage) + 1
        self.embed.description = f'There are {rowcount} level in the list.'
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
        
        
        while True:
            try:
                cur.execute(f'select * from levels where levelID between {self.felid} and {self.lelid} order by levelID')
                for row in cur:
                    self.embed.add_field(name=row[1], value = 'Difficulty : ' + self.diffList[row[3]], inline=False)
                self.embed.set_footer(text='sent by ' + interaction.user.name + f' | Page {(int)(self.felid / self.perpage) + 1} / {pgcount}', icon_url=interaction.user.display_avatar)
                await interaction.edit_original_response(embed = self.embed)  
                await interaction.client.wait_for("reaction_add", check = check, timeout = 15)
                
                if self.rct.emoji == '⬅️':
                    self.felid -= self.perpage
                    if self.felid < 1 : self.felid = 1
                elif self.rct.emoji == '➡️':
                    self.felid += self.perpage
                    if self.felid > rowcount : self.felid = rowcount - (rowcount % self.perpage) + 1
                self.lelid = self.felid + self.perpage - 1
                await self.rct.remove(self.user)
                
                flen = len(self.embed.fields)
                for idx in range(0, flen):
                    self.embed.remove_field(0)
            except asyncio.TimeoutError:
                break
        
        await msg.remove_reaction('⬅️', self.bot.user)
        await msg.remove_reaction('➡️', self.bot.user)
        self.SQLConnection.close()
    
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        read_database(bot)
    )