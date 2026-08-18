from nextcord.http import Route
from nextcord import SlashOption, slash_command
from nextcord.ext import commands
from nextcord.interactions import Interaction

from bot.chaloeilBot import ChaloeilBot
from models.raid import RaidInfo


class Raid(commands.Cog):
    def __init__(self, bot: ChaloeilBot):
        self.bot = bot

    raid_choices = SlashOption(
        name="raid_name",
        description="Le nom du raid pour lequel vous voulez créer un sondage",
        choices={
            "Sanctuaire des Jardins éternels": "belladone",
            "Gouffre du Gigalodon": "gigalodon",
        },
    )

    @slash_command(name="raid_poll", description="Affiche le sondage pour le raid")
    async def raid_poll(
        self, interaction: Interaction[ChaloeilBot], raid_name: str = raid_choices
    ) -> None:
        """Affiche le sondage pour le raid."""
        await interaction.response.defer()
        emoji = self.bot.ch_emojis.get("delire")
        emoji_name = emoji.name if emoji else "✅"
        poll = RaidInfo.get_raid_poll_payload(raid_name, emoji_name)
        await self.bot.http.request(
            Route(
                "POST",
                f"/channels/{interaction.channel_id}/messages",
                channel_id=interaction.channel_id,
            ),
            json=poll,
        )

        await interaction.followup.send(
            f"Sondage pour le raid **{raid_name}** créé avec succès !",
            ephemeral=True,
        )


def setup(bot: ChaloeilBot):
    bot.add_cog(Raid(bot))
