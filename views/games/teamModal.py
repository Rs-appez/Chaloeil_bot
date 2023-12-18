from nextcord.ui import Modal, TextInput


class TeamModal(Modal):

    def __init__(self, view,players) -> None:
        super().__init__('Make your team')

        self.view = view
        self.players = players

        self.team_name = TextInput('Team Name', placeholder='Team Name',required=True)

        self.add_item(self.team_name)

    async def callback(self, interaction):
        await self.view.add_team(self.team_name.value,self.players)


