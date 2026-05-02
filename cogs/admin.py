from nextcord import slash_command
from nextcord.ext import commands
from nextcord.interactions import Interaction

from bot.chaloeilBot import ChaloeilBot
from config import EVENT_ROLE_ID


class Admin(commands.Cog):
    """Admin cmd"""

    def __init__(self, bot):
        self.bot = bot

    @slash_command(default_member_permissions=0)
    async def reset_event_role(
        self,
        interaction: Interaction[ChaloeilBot],
    ) -> None:
        """Reset le rôle d'événement en supprimant tous les membres qui l'ont."""

        event_role = interaction.guild.get_role(int(EVENT_ROLE_ID))
        if not event_role:
            _ = await interaction.response.send_message(
                "Le rôle d'événement n'a pas été trouvé sur ce serveur.",
                ephemeral=True,
            )
            return

        for member in [member for member in event_role.members]:
            await member.remove_roles(event_role)

        _ = await interaction.response.send_message(
            "Le rôle d'événement a été réinitialisé.",
            ephemeral=True,
        )


def setup(bot):
    bot.add_cog(Admin(bot))
