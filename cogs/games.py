from nextcord import (
    ChannelType,
    InteractionContextType,
    Member,
    SlashOption,
    TextChannel,
    slash_command,
)
from nextcord.ext import commands
from nextcord.interactions import Interaction
from nextcord.threads import Thread

from bot.chaloeilBot import ChaloeilBot
from config import EVENT_ROLE_ID
from models.games.battleRoyal import BattleRoyal
from models.games.dice import Dice
from models.games.qotd import QuestionsOfTheDay
from models.games.qotdscheduler import QOTDScheduler
from models.games.question import Question
from models.games.quizz import Quizz
from models.games.teamMaker import TeamMaker
from views.games.joinGameView import JoinGameView
from views.games.makeTeam import MakeTeamView
from views.games.statementView import StatementView


class Game(commands.Cog):
    """some games"""

    choices = {
        "Seulement les maps": "map",
        "Seulement les succès": "succes",
        "Seulement les archimonstres": "archimonstre",
        "Seulement les quêtes": "quete",
        "Seulement les items": "item",
        "Seulement les sorts": "sort",
        "Seulement la géographie": "géographie",
        "Seulement l'élevage": "elevage",
    }

    def __init__(self, bot):
        self.bot = bot
        self.qotd_scheduler = QOTDScheduler(bot)
        self.team_maker: TeamMaker = None

    @slash_command(default_member_permissions=0)
    async def reset_event_role(
        self,
        interaction: Interaction[ChaloeilBot],
    ) -> None:
        """Reset le rôle d'événement en supprimant tous les membres qui l'ont."""

        guild = interaction.guild
        if not guild:
            _ = await interaction.response.send_message(
                "Cette commande doit être utilisée dans un serveur.",
                ephemeral=True,
            )
            return
        event_role = guild.get_role(int(EVENT_ROLE_ID))
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

    @slash_command(
        name="battle_royal_quizz",
        description="Get the 👑",
        contexts=[InteractionContextType.guild],
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
        time_to_answer: int = SlashOption(
            name="time_to_answer",
            description="Time to answer",
            required=False,
            default=20,
        ),
    ):
        """Start a battle royal quizz game"""

        await interaction.response.defer(ephemeral=True)

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
            time_to_answer=time_to_answer,
        )

        await self.__init_game(interaction, br, channel)

    @slash_command(
        name="quizz_battle",
        description="Get the 🪜",
        contexts=[InteractionContextType.guild],
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
        event: bool = SlashOption(name="event", default=False),
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
        id_range: str = SlashOption(
            name="id_range",
            description="Range of question id (ex: 1-10)",
            required=False,
            default=None,
        ),
        time_to_answer: int = SlashOption(
            name="time_to_answer",
            description="Time to answer",
            required=False,
            default=20,
        ),
        spectator: str = SlashOption(
            name="spectator",
            description="Spectator",
            required=False,
            default=None,
        ),
    ):
        """Start a quizz battle game"""

        await interaction.response.defer(ephemeral=True)

        channel = await self.__create_game_channel(interaction, "quizz battle")
        if not channel:
            return

        quizz = Quizz(
            channel,
            interaction.user.id,
            category,
            nb_question,
            team=team,
            event=event,
            flat=flat,
            keep=keep,
            debug=debug,
            id_range=id_range,
            time_to_answer=time_to_answer,
            spectator_players_ids=[int(s) for s in spectator.split(",")]
            if spectator
            else [],
        )

        await self.__init_game(interaction, quizz, channel)

    @slash_command(
        name="question",
        description="Ask one question",
        contexts=[InteractionContextType.guild],
        default_member_permissions=0,
    )
    async def question(
        self,
        interaction: Interaction,
        player: Member = SlashOption(
            name="player",
            description="Select a player",
            required=True,
        ),
        category: str = SlashOption(
            name="categorie",
            description="Choisi une categorie",
            required=False,
            choices=choices,
        ),
    ):
        """Ask one question"""
        await interaction.response.defer()
        question = await Question.get_question(1, cat=category)
        if question:
            await interaction.followup.send("Question pour " + player.mention + " !!!")
            if isinstance(interaction.channel, (Thread, TextChannel)):
                await question[0].ask_standalone(
                    player=player, channel=interaction.channel
                )

        else:
            await interaction.followup.send(
                "Erreur lors de la récupération de la question 😭"
            )

    @slash_command(
        name="dice",
        description="Roll the dice 🎲",
    )
    async def dice(
        self,
        interaction: Interaction,
        number_of_dice: int = SlashOption(
            name="nombre_de_dés",
            description="Nombre de dés à lancer",
            required=False,
            default=1,
        ),
        sides: int = SlashOption(
            name="nombre_de_faces",
            description="Nombre de faces des dés",
            required=False,
            default=6,
        ),
    ):
        """Roll the dice"""

        _ = await interaction.response.send_message(
            "Les dés sont jetés !", ephemeral=True
        )
        dice = Dice(number_of_dice, sides)
        username = interaction.user.nick or interaction.user.name
        _ = await interaction.channel.send(dice.verbal_roll(username))
        _ = await interaction.channel.send(dice.image_roll())

    @slash_command(
        name="daily_quizz",
        description="Get the daily quizz",
        contexts=[InteractionContextType.guild],
    )
    async def daily_quizz(self, interaction: Interaction):
        """Get the daily quizz"""

        try:
            await interaction.response.defer(ephemeral=True)
            channel = await self.__create_game_channel(interaction, "daily quizz")

            if not channel:
                raise Exception("Channel creation failed")

            qotd = await QuestionsOfTheDay.create(channel, interaction.user.id)
            chaloeil_emoji = (
                self.bot.ch_emojis["chaloeil"]
                if "chaloeil" in self.bot.ch_emojis
                else None
            )

            await qotd.launch_statement()
            await interaction.followup.send(
                f"{chaloeil_emoji} **Démarre la série de questions du jour !** {chaloeil_emoji}",
                view=JoinGameView(qotd, chaloeil_emoji),
                ephemeral=True,
            )

        except ValueError:
            await interaction.followup.send(
                "Les questions du jour ne sont pas encore disponibles. Veuillez réessayer plus tard. <:chaloeil:1386369580275994775>",
                ephemeral=True,
            )
            if channel:
                _ = await channel.delete()

        except Exception as e:
            await interaction.followup.send(
                f"Une erreur est survenue lors de la création du Quizz du jour : {
                    str(e)
                }",
                ephemeral=True,
            )
            if channel:
                _ = await channel.delete()

    @slash_command(
        name="setup_team_maker",
        description="Créer une équipe pour les jeux en équipe",
        contexts=[InteractionContextType.guild],
        default_member_permissions=0,
    )
    async def setup_team_maker(
        self,
        interaction: Interaction,
        nb_players_per_team: int = SlashOption(
            name="nombre_de_joueurs_par_équipe",
            description="Nombre de joueurs par équipe",
            required=True,
        ),
    ):
        """Créer les équipes pour les jeux en équipe"""
        if self.team_maker:
            _ = await interaction.response.send_message(
                "Les équipes ont déjà été setup", ephemeral=True
            )
            return
        _ = await interaction.response.send_message(
            view=MakeTeamView(self, interaction.user, nb_players_per_team)
        )

    @slash_command(
        name="show_teams",
        description="Afficher les équipes créées pour les jeux en équipe",
        contexts=[InteractionContextType.guild],
        default_member_permissions=0,
    )
    async def show_teams(self, interaction: Interaction):
        if not self.team_maker:
            _ = await interaction.response.send_message(
                "Les équipes n'ont pas encore été setup", ephemeral=True
            )
            return

        _ = await interaction.response.defer()
        teams = self.team_maker.make_teams()
        message = "Voici les équipes :\n"
        for i, t in enumerate(teams):
            message += (
                f"**Equipe {i + 1}** : "
                + ", ".join([m.member.mention for m in t])
                + "\n"
            )
        await interaction.followup.send(message)

    @slash_command(
        name="reset_teams",
        description="Reset les équipes créées pour les jeux en équipe",
        contexts=[InteractionContextType.guild],
        default_member_permissions=0,
    )
    async def reset_teams(self, interaction: Interaction):
        """Reset les équipes créées pour les jeux en équipe"""
        self.team_maker = None
        _ = await interaction.response.send_message(
            "Les équipes ont été réinitialisées.", ephemeral=True
        )

    async def __create_game_channel(self, interaction: Interaction, name_channel):
        if not interaction.channel:
            _ = await interaction.followup.send(
                "Impossible de créer un channel de jeu dans ce contexte", ephemeral=True
            )
            return None
        if interaction.channel.type in [
            ChannelType.news_thread,
            ChannelType.public_thread,
            ChannelType.private_thread,
        ]:
            _ = await interaction.followup.send(
                "Tu ne peux pas lancer un jeu dans un thread", ephemeral=True
            )
            return None

        channel = interaction.channel

        if channel.type == ChannelType.private:
            game_channel = interaction.channel
        elif isinstance(channel, TextChannel):
            game_channel = await channel.create_thread(
                name=name_channel,
                reason=f"{name_channel} started",
                type=ChannelType.private_thread,
            )
        else:
            _ = await interaction.followup.send(
                "Type de channel non supporté pour lancer un jeu", ephemeral=True
            )
            return None
        return game_channel

    async def __init_game(self, interaction: Interaction, game: Quizz, game_channel):
        chaloeil_emoji = (
            self.bot.ch_emojis["chaloeil"] if "chaloeil" in self.bot.ch_emojis else None
        )
        delire_blason = (
            self.bot.ch_emojis["delire"] if "delire" in self.bot.ch_emojis else None
        )

        await game_channel.send(
            f"{delire_blason} {chaloeil_emoji} WELCOME {chaloeil_emoji} {delire_blason}"
        )
        if isinstance(interaction.channel, (Thread, TextChannel)):
            _ = await interaction.channel.send(
                f"{chaloeil_emoji} **Participez au grand quiz du Chaloeil !** {chaloeil_emoji}",
                view=JoinGameView(game, chaloeil_emoji),
            )
            await interaction.followup.send(
                "Afficher l'énoncé", view=StatementView(game), ephemeral=True
            )

    @commands.Cog.listener()
    async def on_ready(self):
        # self.qotd_scheduler.start()
        pass


def setup(bot):
    bot.add_cog(Game(bot))
