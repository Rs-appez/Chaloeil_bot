from nextcord.ext import commands
from nextcord import slash_command
from nextcord import SlashOption

from models.fm.runes import Rune


class Fm(commands.Cog):
    """Admin cmd"""

    stats = {
        "Force": "fo",
        "Intelligence": "ine",
        "Agilité": "age",
        "Chance": "cha",
        "Vitalité": "vi",
        "Initiative": "ini",
        "Puissance": "pui",
        "Résistance  élémentaire/mélée/distance": "ré per",
        "Résistance poussée": "ré pou",
        "Résistance critique": "ré cri",
        "Retrait": "ret",
        "Pods": "pod",
        "Tacle/fuite": "tac/fui",
        "Dommages élémentaires": "do",
        "Dommages poussée/critique": "do cri",
        "Soins": "so",
        "Critique": "cri",
        "Dommages distance": "do per di",
        "Dommages mêlée": "do per mé",
        "Dommages arme": "do per ar",
        "Dommages sort": "do per so",
    }

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="trans_info", description="Get the transcendence info")
    async def transMax(
        self,
        interaction,
        stat: str = SlashOption(
            name="statistique",
            description="Statistique à transcender",
            required=False,
            choices=stats,
        ),
    ):
        if stat:
            info = Rune.get_rune_info(stat)
            await interaction.response.send_message(f"{info}")
        else:
            info = Rune.get_all_rune_info()
            await interaction.response.send_message(f"{info}", ephemeral=True)

    @slash_command(
        name="trans_info_image", description="Get the transcendence info image"
    )
    async def transMaxImage(self, interaction):
        await interaction.response.send_message(Rune.image_url, ephemeral=True)


def setup(bot):
    bot.add_cog(Fm(bot))
