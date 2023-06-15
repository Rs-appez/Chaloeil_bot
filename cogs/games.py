from nextcord.ext import commands
from nextcord.interactions import Interaction
from nextcord import slash_command
from models.games.battleRoyal import BattleRoyal

class Game(commands.Cog):
    """some games"""

    def __init__(self,bot):
        self.bot = bot


    @slash_command(name="battle_royal",description="Get the 👑",dm_permission=False)
    async def br(self,interaction : Interaction ):
        br = BattleRoyal(interaction.channel)
        await br.start()
        await interaction.response.send_message("ok")



def setup(bot):
    bot.add_cog(Game(bot))