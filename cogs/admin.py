from nextcord.ext import commands
from nextcord import slash_command, ChannelType


class Admin(commands.Cog):
    """Admin cmd"""

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="delete_messages",
        description="Delete a messages in a channel",
        default_member_permissions=1,
    )
    async def delete_messages(self, interaction, message_id: str):
        """Delete a message by its"""
        try:
            message = await interaction.channel.fetch_message(message_id)
            if message:
                await message.delete()
                await interaction.response.send_message(
                    "Message deleted successfully.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Message not found.", ephemeral=True
                )
        except Exception as e:
            return interaction.response.send_message(
                f"An error occurred: {str(e)}", ephemeral=True
            )


def setup(bot):
    bot.add_cog(Admin(bot))
