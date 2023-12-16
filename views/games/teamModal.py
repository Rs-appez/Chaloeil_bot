from nextcord.ui import Modal, TextInput
from models.games.team import Team


class TeamModal(Modal):

    def __init__(self, quizz,players) -> None:
        super().__init__('Make your team')

        self.quizz = quizz
        self.players = players

        self.team_name = TextInput('Team Name', placeholder='Team Name',required=True)

        self.add_item(self.team_name)

    async def callback(self, interaction):
        await self.quizz.add_team(Team(self.team_name.value,self.players))


