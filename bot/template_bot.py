import bot_config
import discord
import re

from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='+', intents=intents)
bot.remove_command('help') # Will replace this with our custom help command

activity = discord.Activity(type=discord.ActivityType.listening, name='commands')
CONFIG = bot_config.BotConfig(bot=bot)

initial_extensions = []
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

def can_reload(ctx):
    user_id = ctx.message.author.id
    return (user_id == CONFIG.OWNER_ID)

@bot.command(name='help')
@commands.dm_only()
async def help(ctx):
    help_text = """
Welcome to the bot!

See below for commands you can use.

```
+command
```
"""

    await ctx.send(content=help_text)

@bot.command(name='reload')
@commands.check(can_reload)
async def reload(ctx):
    for extension in initial_extensions:
        bot.reload_extension(extension)

    await ctx.message.author.send(content='Reloaded the bot!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')

@bot.event
async def on_command_error(ctx, error):
    err = getattr(error, 'original', error)

    if isinstance(err, commands.MissingAnyRole):
        return
    if isinstance(err, commands.PrivateMessageOnly):
        return
    if isinstance(err, commands.CheckFailure):
        await ctx.send(content='You do not have permission to use that command!')
        return
    if isinstance(err, commands.CommandNotFound):
        command = ctx.message.content.split(" ")[0]
        command_safe = re.sub(r'<@[!&]?\d+>', '', command)
        await ctx.send(content="Sorry, I don't know the command {0}".format(command_safe))
        return
    
    raise error

bot.run(CONFIG.TOKEN)