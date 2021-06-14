import discord
import json
import os.path

class BotConfig:
    def __init__(self, bot=None, file='config.json'):
        self.bot = bot

        if not os.path.exists(file):
            raise FileNotFoundError('Could not find configuration file: ' + file)
        
        with open(file) as f:
            try:
                config_dict = json.load(f)
            except Exception as e:
                raise Exception('Error while parsing ' + file + ': ' + str(e))
        
        try:
            try:
                self.ADMIN_IDS = [int(x) for x in config_dict['ADMIN_ROLES']]
            except ValueError as e:
                raise ValueError('Error while parsing ADMIN_ROLES: ' + str(e))
            
            try:
                self.MASTER_GUILD = int(config_dict['MASTER_GUILD'])
            except ValueError as e:
                raise ValueError('Error while parsing MASTER_GUILD: ' + str(e))

            self.TOKEN = config_dict['TOKEN']
            if self.TOKEN == '':
                raise ValueError('Error while parsing TOKEN: No value specified')

        except KeyError as e:
            raise KeyError(str(e) + ' missing from ' + file)
    
    def GET_GUILD(self, guild_id: int):
        if self.bot is None:
            raise ValueError('BotConfig bot is not defined')

        guild = discord.utils.get(self.bot.guilds, id=guild_id)
        if guild is None:
            raise ValueError('Bot is not a member of guild ' + guild_id)
        
        return guild

    def get_guild_text_channel(self, guild_id: int, channel_id: int):
        guild = self.GET_GUILD(guild_id)
        return discord.utils.get(guild.text_channels, id=channel_id)

    def get_guild_member(self, guild_id: int, member_id: int):
        guild = self.GET_GUILD(guild_id)
        return guild.get_member(member_id)
    
    def get_guild_role_by_name(self, guild_id: int, role_name: str):
        guild = self.GET_GUILD(guild_id)
        return discord.utils.get(guild.roles, name=role_name)

    def get_guild_role_by_id(self, guild_id: int, role_id: int):
        guild = self.GET_GUILD(guild_id)
        return discord.utils.get(guild.roles, id=role_id)
    
    def get_user_full_name(self, discord_user):
        if discord_user is None:
            return None
        else:
            return "{0}#{1}".format(discord_user.name, discord_user.discriminator)