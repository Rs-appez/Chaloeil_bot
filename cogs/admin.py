from nextcord.ext import commands
from nextcord import slash_command
from interaction_discord_bot.message import Interaction

class Admin(commands.Cog):
    """Admin cmd"""
    def __init__(self,bot):
        self.bot = bot

                    
def setup(bot):
    bot.add_cog(Admin(bot))
    bot.add_cog(Interaction(bot))