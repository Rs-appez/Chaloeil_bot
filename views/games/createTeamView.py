from nextcord import ButtonStyle
from nextcord.ui import View, button

from views.games.teamModal import TeamModal
from nextcord.ui import Select , UserSelect, UserSelectValues
from nextcord import SelectOption
from models.games.team import Team

class CreateTeamView(View):

    def __init__(self,game,list_team_msg) -> None:
        super().__init__(timeout=None)

        self.game = game
        self.list_team_msg = list_team_msg

        self.players = [SelectOption(label=str(player)) for player in self.game.players]
        max_values = len(self.players) if len(self.players) < 4 else 4

        self.team_name = None
        self.team_members = Select(placeholder='Team Members',min_values=1,max_values=max_values,options=self.players)

        self.add_item(self.team_members)

    async def add_team(self,team_name,team_members):

        team_members = [player for player in self.game.players if str(player) in team_members]
        
        await self.game.add_team(Team(team_members,team_name))

        list_team = "Liste des équipes : \n"

        for team in self.game.teams:
            list_team += f"> {team}\n"

        await self.list_team_msg.edit(content=list_team)

    @button(label='Team', style=ButtonStyle.primary,emoji="🆕")
    async def make_team(self,button,interaction):

        await interaction.response.send_modal(TeamModal(self,self.team_members.values))


    @button(label="START !",style=ButtonStyle.primary)
    async def start(self,button,interaction):

        if interaction.user.id == self.game.creator_id :
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await self.game.show_question()

        else :
            await interaction.response.send_message("Seul celui qui a démarré le jeu peut le lancer.",ephemeral=True)