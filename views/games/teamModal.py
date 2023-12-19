from nextcord.ui import Modal, TextInput
from nextcord import TextInputStyle


class TeamModal(Modal):

    def __init__(self, view,players) -> None:
        super().__init__('Make your team')

        self.view = view
        self.players = players

        self.team_name = TextInput('Team Name', placeholder='Team Name',required=True)

        self.players_list = "".join([f"{i+1} - {player}\n" for i,player in enumerate(players)])

        self.players_display= TextInput('Players', placeholder='Players',default_value=self.players_list,style=TextInputStyle.paragraph,required=True)

        self.add_item(self.team_name)
        self.add_item(self.players_display)

    async def callback(self, interaction):
        await self.view.add_team(self.team_name.value,self.players,interaction)


