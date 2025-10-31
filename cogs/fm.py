from nextcord.ext import commands
from nextcord import slash_command
from nextcord import SlashOption


class Fm(commands.Cog):
    """Admin cmd"""

    stats = {
        "force/intelligence/agilité/chance": "baseStats",
        "vitalité": "vi",
        "initiative": "ini",
        "puissance": "pui",
        "résistance  élémentaire": "rePer",
        "résistance poussée": "rePou",
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
        await interaction.response.send_message(
            f"La statistique {stat} peut être transcendée jusqu'à +20."
        )


def setup(bot):
    bot.add_cog(Fm(bot))
