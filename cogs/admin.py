from nextcord.ext import commands
from nextcord import slash_command

from views.admin.speakModal import SpeakModal

class Admin(commands.Cog):
    """Admin cmd"""
    def __init__(self,bot):
        self.bot = bot

    
    @slash_command(description="🎙️",dm_permission=False,default_member_permissions= 0)
    async def speak(self, interaction, message : str = None):
        """Send a message in a channel"""
        if message :
            try:
                await interaction.channel.send(message)
                await interaction.response.send_message("Message sent !",ephemeral=True)
            except Exception as e:          
                await interaction.response.send_message(f"Error : {e}",ephemeral=True)
        else :
            await interaction.response.send_modal(SpeakModal(self.bot,interaction.channel.id))
                    
def setup(bot):
    bot.add_cog(Admin(bot))