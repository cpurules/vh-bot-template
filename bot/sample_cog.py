import asyncio
import bot_config
import discord

from discord.ext import commands

CONFIG = bot_config.BotConfig()

class SampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(SampleCog(bot))
    CONFIG.bot = bot