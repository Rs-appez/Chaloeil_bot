from nextcord.ext import commands
from nextcord.interactions import Interaction
from nextcord import slash_command, ChannelType
from models.games.battleRoyal import BattleRoyal
from models.games.quizz import Quizz
from views.games.joinGameView import JoinGameView
from views.games.statementView import StatementView
from nextcord import SlashOption


class Game(commands.Cog):
    """some games"""

    choices = {
        "Seulement les maps": "map",
        "Seulement les succès": "succes",
        "Seulement les archimonstres": "archimonstre",
        "Seulement les quêtes": "quete",
        "Seulement les items": "item",
        "Seulement les sorts": "sort",
    }

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="battle_royal_quizz",
        description="Get the 👑",
        dm_permission=False,
        default_member_permissions=0,
    )
    async def br(
        self,
        interaction: Interaction,
        category: str = SlashOption(
            name="categorie",
            description="Choisi une categorie",
            required=False,
            choices=choices,
        ),
        team: bool = SlashOption(
            name="team", description="Jouer en équipe", required=False, default=False
        ),
        life_point: int = SlashOption(
            name="point_de_vie",
            description="Nombre de point de vie",
            required=False,
            default=3,
        ),
        keep: bool = SlashOption(
            name="keep",
            description="Garder le thread après la partie",
            required=False,
            default=False,
        ),  
        debug: bool = SlashOption(
            name="debug",
            description="Display id question",
            required=False,
            default=False,
        ),
    ):
        """Start a battle royal quizz game"""

        channel = await self.__create_game_channel(interaction, "battle royal")
        if not channel:
            return

        br = BattleRoyal(
            channel,
            interaction.user.id,
            category,
            team=team,
            life_point=life_point,
            keep=keep,
            debug=debug,
        )

        await self.__init_game(interaction, br, channel)

    @slash_command(
        name="quizz_battle",
        description="Get the 🪜",
        dm_permission=False,
        default_member_permissions=0,
    )
    async def quizz(
        self,
        interaction: Interaction,
        nb_question: int,
        category: str = SlashOption(
            name="categorie",
            description="Choisi une categorie",
            required=False,
            choices=choices,
        ),
        team: bool = SlashOption(
            name="team", description="Jouer en équipe", required=False, default=False
        ),
        flat: bool = SlashOption(
            name="flat",
            description="Jouer en flat (toutes les questions raportent le même nombre de point)",
            required=False,
            default=False,
        ),
        keep: bool = SlashOption(
            name="keep",
            description="Garder le thread après la partie",
            required=False,
            default=False,
        ),
        debug: bool = SlashOption(
            name="debug",
            description="Display id question",
            required=False,
            default=False,
        ),
    ):
        """Start a quizz battle game"""

        channel = await self.__create_game_channel(interaction, "quizz battle")
        if not channel:
            return

        quizz = Quizz(
            channel,
            interaction.user.id,
            category,
            nb_question,
            team=team,
            flat=flat,
            keep=keep,
            debug=debug,
        )

        await self.__init_game(interaction, quizz, channel)

    async def __create_game_channel(self, interaction: Interaction, name_channel):
        if interaction.channel.type in [
            ChannelType.news_thread,
            ChannelType.public_thread,
            ChannelType.private_thread,
        ]:
            await interaction.response.send_message(
                "Tu ne peux pas lancer un jeu dans un thread", ephemeral=True
            )
            return None

        if interaction.channel.type == ChannelType.private:
            game_channel = interaction.channel
        else:
            game_channel = await interaction.channel.create_thread(
                name=name_channel,
                reason=f"{name_channel} started",
                type=ChannelType.private_thread,
            )
        return game_channel

    async def __init_game(self, interaction: Interaction, game, game_channel):
        chaloeil_emoji = (
            self.bot.ch_emojis["chaloeil"] if "chaloeil" in self.bot.ch_emojis else None
        )
        delire_blason = (
            self.bot.ch_emojis["delire"] if "delire" in self.bot.ch_emojis else None
        )

        await game_channel.send(
            f"{delire_blason} {chaloeil_emoji} WELCOME {chaloeil_emoji} {delire_blason}"
        )
        await interaction.channel.send(
            f"{chaloeil_emoji} **Participez au grand quiz du Chaloeil !** {chaloeil_emoji}",
            view=JoinGameView(game, chaloeil_emoji),
        )
        await interaction.response.send_message(
            "Afficher l'énoncé", view=StatementView(game), ephemeral=True
        )


def setup(bot):
    bot.add_cog(Game(bot))
