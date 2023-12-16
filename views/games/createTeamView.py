from nextcord import ButtonStyle
from nextcord.ui import View, button

from views.games.teamModal import TeamModal
from nextcord.ui import UserSelect, TextInput
from nextcord import SelectOption

class CreateTeamView(View):

    def __init__(self,game) -> None:
        super().__init__()

        self.game = game

        self.team_name = None
        self.team_members = UserSelect(placeholder='Team Members',min_values=1,max_values=4)

        self.add_item(self.team_members)

    @button(label='Créer', style=ButtonStyle.primary,emoji="🆕")
    async def statement(self,button,interaction):

        await interaction.response.send_modal(TeamModal(self.game,self.team_members.values))


    @button(label="START !",style=ButtonStyle.primary)
    async def start(self,button,interaction):

        if interaction.user.id == self.game.creator_id :
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await self.game.show_question()

        else :
            await interaction.response.send_message("Seul celui qui a démarré le jeu peut le lancer.",ephemeral=True)