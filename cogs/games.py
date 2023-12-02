from nextcord.ext import commands
from nextcord.interactions import Interaction
from nextcord import slash_command , ChannelType 
from models.games.battleRoyal import BattleRoyal
from views.games.joinGameView import JoinGameView
from views.games.statementView import StatementView
from nextcord import SlashOption

class Game(commands.Cog):
    """some games"""

    choices = {
        "Seulement les maps" : "map",
        "Seulement les succès" : "succes",
    }

    def __init__(self,bot):
        self.bot = bot


    @slash_command(name="battle_royal_quizz",description="Get the 👑",dm_permission=False,default_member_permissions= 0)
    async def br(self,interaction : Interaction, category  : str = SlashOption(name="categorie",description="Choisi une categorie",required=False,choices=choices) ):
        """Start a battle royal quizz game"""
        
        channel = await self.__create_game_channel(interaction,"battle royal")
        if not channel :
            return 
        
        br = BattleRoyal(channel,interaction.user.id,category)

        chaloeil_emoji = self.bot.ch_emojis["chaloeil"] if "chaloeil"  in self.bot.ch_emojis else None
        delire_blason = self.bot.ch_emojis['delire'] if "delire" in self.bot.ch_emojis else None

        await channel.send(f"{delire_blason} {chaloeil_emoji} WELCOME {chaloeil_emoji} {delire_blason}")
        await interaction.channel.send("Rejoint la partie !",view=JoinGameView(br,chaloeil_emoji))
        await interaction.response.send_message("Afficher l'énoncé",view=StatementView(br),ephemeral=True)


    async def __create_game_channel(self,interaction : Interaction,name_channel):

        if interaction.channel.type in [ChannelType.news_thread,ChannelType.public_thread,ChannelType.private_thread] :
            await interaction.response.send_message("Tu ne peux pas lancer un jeu dans un thread",ephemeral=True)
            return None
        
        if interaction.channel.type == ChannelType.private :
            game_channel = interaction.channel
        else :
            game_channel = await interaction.channel.create_thread(name=name_channel,reason = f"{name_channel} started",type=ChannelType.private_thread)
        return game_channel


def setup(bot):
    bot.add_cog(Game(bot))