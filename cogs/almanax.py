from nextcord import SlashOption, slash_command
from nextcord.ext import commands
from nextcord.interactions import Interaction

from models.almanax.ecocraft import EcoCraft
from bot.chaloeilBot import ChaloeilBot


class Almanax(commands.Cog):
    JOBS = {
        "Eleveur": "Breeder",
        "Bûcheron": "Lumberjack",
        "Chasseur": "Hunter",
        "Pêcheur": "Fisherman",
        "Mineur": "Miner",
        "Paysans": "Farmer",
        "Bricoleur": "Handyman",
        "Alchimiste": "Alchemist",
        "Forgeron": "Smith",
        "Bijoutier": "Jeweller",
        "Cordonnier": "Shoemaker",
        "Tailleur": "Tailor",
        "Sculpteur": "Carver",
        "Faconneur": "Artificer",
    }

    job_choices = SlashOption(
        name="métier",
        description="Le métier pour lequel vous voulez connaître le jour de l'écocraft",
        choices=JOBS,
        required=False,
    )

    def __init__(self, bot: ChaloeilBot):
        self.bot = bot

    @slash_command(name="ecocraft", description="Affiche le jour de l'écocraft")
    async def ecocraft(
        self,
        interaction: Interaction[ChaloeilBot],
        metier: str = job_choices,
    ) -> None:
        """Affiche l'almanax du jour."""
        if not metier:
            dates = EcoCraft.get_all_dates()
            message = "Voici les jours de l'écocraft pour tous les métiers :\n"
            for bonus, day, month in dates:
                message += f"> **{day}/{month}** : {bonus}\n"
            _ = await interaction.response.send_message(message, ephemeral=True)

        else:
            eco_craft = EcoCraft(metier)
            date = eco_craft.get_date()
            _ = await interaction.response.send_message(
                f"Le jour de l'écocraft pour le métier {next((k for k, v in self.JOBS.items() if v == metier))} est le  **{date[0]}/{date[1]}**",
                ephemeral=True,
            )


def setup(bot: ChaloeilBot):
    bot.add_cog(Almanax(bot))
