from nextcord.ext import commands
from nextcord import slash_command

from views.admin.speakModal import SpeakModal

class Admin(commands.Cog):
    """Admin cmd"""
    def __init__(self,bot):
        self.bot = bot

    
    @slash_command(description="🎙️",dm_permission=False,default_member_permissions= 0)
    async def speak(self, interaction):
        """Send a message in a channel"""
        await interaction.response.send_modal(SpeakModal(self.bot))
                    
def setup(bot):
    bot.add_cog(Admin(bot))