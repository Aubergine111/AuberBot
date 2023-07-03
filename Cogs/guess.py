from discord import app_commands, Interaction, Embed
from discord.ext import commands
import discord.ext.tasks
import random
import datetime
import pytz
import sqlite3
import asyncio
import time
import numpy as np

class guess(commands.Cog):
    difflist = []
    def __init__(self, bot:commands.Bot) -> None :
        self.rng = np.random.default_rng((int)(time.time()))
        self.bot = bot
        self.diffList = ['None', 'Easy', 'Normal', 'Hard', 'Impossible']
        self.lastRngValue = 0
    
    @app_commands.command(name='guess', description='Guess the ILL level!')
    @app_commands.describe(diff = 'difficulty')
    @app_commands.choices(diff = [
        app_commands.Choice(name = 'None', value = 0),
        app_commands.Choice(name = 'Easy', value = 1),
        app_commands.Choice(name = 'Normal', value = 2),
        app_commands.Choice(name = 'Hard', value = 3),
        app_commands.Choice(name = 'Impossible', value = 4)
    ])
    async def guess(self, interaction : Interaction, diff : app_commands.Choice[int] = 0) -> None:
        self.waitTime = 15
        self.embed = Embed(title='Guess The Level!',
                           description=f'Guess the level in {self.waitTime} second! first to guess wins.',
                           timestamp=datetime.datetime.now(pytz.timezone('UTC')),
                           color=0x0071FF)
        self.embed.set_author(name="AuberBot", icon_url=self.bot.user.display_avatar)
        self.SQLConnection = sqlite3.connect('./test.db', isolation_level=None)
        cur = self.SQLConnection.cursor()
        if not isinstance(diff, int) and diff.value != 0:
            cur.execute(f'select * from levels where diff = {diff.value}')
        else:
            cur.execute('select * from levels')
        rows = cur.fetchall()
        rowcount = len(rows)
        if rowcount <= 0 :
            self.embed.add_field(name='No level exist in that difficulty', value = ':/', inline=False)
        else:
            rints = self.rng.integers(0, rowcount, 1)
            while rints == self.lastRngValue:
                rints = self.rng.integers(0, rowcount, 1)
            print(rints)
            row = rows[rints[0]]
            print(row)
            self.embed.add_field(name='Difficulty : ' + self.diffList[row[3]], value = ' ', inline=False)
            self.embed.set_image(url=row[2])
        try :
            self.embed.set_footer(text='sent by ' + interaction.user.name, icon_url=interaction.user.display_avatar)
        except discord.errors.HTTPException:
            self.embed.set_footer(text='sent by ' + interaction.user.name)
        await interaction.response.send_message(embed = self.embed)
        if rowcount <= 0 : return
        self.SQLConnection.close()
        def check(m:discord.Message):
                return m.channel.id == interaction.channel.id
        
        msg = await interaction.original_response()
        start = time.time()
        while time.time() < start + self.waitTime:
            try:
                responce = await interaction.client.wait_for("message", check = check, timeout=start + self.waitTime - time.time())
                if responce.content.lower() == row[1].lower():
                    await msg.reply("Correct, <@" + str(responce.author.id) + ">! the answer is " + row[1] + '.')
                    return 
            except asyncio.TimeoutError:
                break
        await msg.reply("Time's over! the answer is " + row[1] + '.')
    
    
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        guess(bot)
    )