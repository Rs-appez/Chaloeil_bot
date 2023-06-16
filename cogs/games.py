from nextcord.ext import commands
from nextcord.interactions import Interaction
from nextcord import slash_command , ChannelType
from models.games.battleRoyal import BattleRoyal
from views.games.joinGameView import JoinGameView

class Game(commands.Cog):
    """some games"""

    def __init__(self,bot):
        self.bot = bot


    @slash_command(name="battle_royal",description="Get the 👑",dm_permission=False)
    async def br(self,interaction : Interaction ):
        channel = await self.__create_game_channel(interaction,"battle royal")
        br = BattleRoyal(channel)
        await br.start()
        await interaction.response.send_message("Rejoint la partie !",view=JoinGameView(br,self.bot.emoji))


    async def __create_game_channel(self,interaction : Interaction,name_channel):

        if interaction.channel.type == ChannelType.private :
            game_channel = interaction.channel
        else :
            game_channel = await interaction.channel.create_thread(name=name_channel,reason = f"{name_channel} started",type=ChannelType.private_thread)
        return game_channel


def setup(bot):
    bot.add_cog(Game(bot))