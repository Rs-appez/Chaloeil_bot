from nextcord import ButtonStyle
from nextcord.ui import View, button

from models.games.player import Player
from models.games.teamMaker import TeamMaker


class MakeTeamView(View):
    def __init__(self, game_controller, admin, nb_players_per_team) -> None:
        super().__init__(timeout=None)
        self.__controller = game_controller
        self.__admin = admin
        self.__players = set()
        self.__nb_players_per_team = nb_players_per_team

    @button(label="Participez", style=ButtonStyle.blurple)
    async def participate(self, button, interaction):
        await interaction.response.send_message(
            "Vous avez été ajouté à la liste des participants.", ephemeral=True
        )
        self.__players.add(Player(interaction.user))

    @button(label="Valider la liste de jouer", style=ButtonStyle.green)
    async def generate_team(self, button, interaction):
        if interaction.user.id != self.__admin.id:
            await interaction.response.send_message(
                "Seul chaloeil peut valider les équipes.", ephemeral=True
            )
            return

        team_maker = TeamMaker(self.__nb_players_per_team, self.__players)
        self.__controller.team_maker = team_maker

        _ = await interaction.response.send_message(
            "Liste des équipes récupérée", ephemeral=True
        )
