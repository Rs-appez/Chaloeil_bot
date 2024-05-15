from nextcord.ext import commands
from nextcord import slash_command

class Admin(commands.Cog):
    """Admin cmd"""
    def __init__(self,bot):
        self.bot = bot

                    
def setup(bot):
    bot.add_cog(Admin(bot))
