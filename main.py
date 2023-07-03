from discord import Intents
from discord.ext import commands
from discord import Game
from discord import Status
import sqlite3

class AuberBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=Intents.all(),
            sync_command = True,
            application_id = "add your own ID"
        )
        self.initial_extension = [
            'Cogs.ping',
            'Cogs.help',
            'Cogs.insert',
            'Cogs.read-database',
            'Cogs.guess',
            'Cogs.purge',
            'Cogs.remove',
            'Cogs.fetch'
        ]
        self.SQLConnection = sqlite3.connect('./test.db', isolation_level=None)
        cur = self.SQLConnection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS levels (levelID INT PRIMARY KEY, levelName TEXT, imgLnk TEXT, diff INT);")
        self.SQLConnection.close()
        
    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)
        await bot.tree.sync()
        
    async def on_ready(self):
        print('ready!')
        print(self.user.name)
        print(self.user.id)
        print('==================================')
        activity = Game('Being Tested')
        await self.change_presence(status=Status.online, activity=activity)

bot = AuberBot()
bot.run("add your own token")