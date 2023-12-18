from nextcord import ButtonStyle
from nextcord.ui import View, button

from views.games.teamModal import TeamModal
from nextcord.ui import Select , UserSelect, UserSelectValues
from nextcord import SelectOption

class CreateTeamView(View):

    def __init__(self,game) -> None:
        super().__init__()

        self.game = game

        self.players = [SelectOption(label=str(player)) for player in self.game.players]
        max_values = len(self.players) if len(self.players) < 4 else 4

        self.team_name = None
        self.team_members = Select(placeholder='Team Members',min_values=1,max_values=max_values,options=self.players)

        self.add_item(self.team_members)

    @button(label='Team', style=ButtonStyle.primary,emoji="🆕")
    async def make_team(self,button,interaction):

        await interaction.response.send_modal(TeamModal(self.game,self.team_members.values))


    @button(label="START !",style=ButtonStyle.primary)
    async def start(self,button,interaction):

        if interaction.user.id == self.game.creator_id :
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await self.game.show_question()

        else :
            await interaction.response.send_message("Seul celui qui a démarré le jeu peut le lancer.",ephemeral=True)