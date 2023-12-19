from nextcord import ButtonStyle
from nextcord.ui import View, button

from views.games.teamModal import TeamModal
from nextcord.ui import Select
from nextcord import SelectOption
from models.games.team import Team

class CreateTeamView(View):


    def __init__(self,game) -> None:
        super().__init__(timeout=None)

        self.game = game
        

    @button(label='Team', style=ButtonStyle.primary,emoji="🆕")
    async def make_team(self,button,interaction):

        await interaction.response.send_message("*Selectione **tout** les membres de ton équipe dans le menu déroulant*",view=SelectPlayerView(self.game),ephemeral=True)

    @button(label="START !",style=ButtonStyle.primary)
    async def start(self,button,interaction):

        if interaction.user.id == self.game.creator_id :
            for btn in self.children :
                btn.disabled = True
            await interaction.response.edit_message(view=self)
            await self.game.show_question()

        else :
            await interaction.response.send_message("Seul celui qui a démarré le jeu peut le lancer.",ephemeral=True)


class SelectPlayerView(View):

    def __init__(self,game) -> None:
        super().__init__(timeout=None)

        self.game = game

        self.team_name = None

        self.players = [SelectOption(label=str(player)) for player in self.game.players]
        max_values = len(self.players) if len(self.players) < 4 else 4

        self.team_members = Select(placeholder='Team Members',min_values=1,max_values=max_values,options=self.players)
        self.add_item(self.team_members)

    async def add_team(self,team_name,team_members,interaction):

        team_members = [player for player in self.game.players if str(player) in team_members]
        
        if not self.game.add_team(Team(team_members,team_name)):
            await interaction.response.send_message("Certains joueurs sont déjà dans une équipe.",ephemeral=True)
            return

        list_team = "Liste des équipes : \n"

        for team in self.game.teams:
            list_team += f"> {team}\n"

        await self.game.list_team_msg.edit(content=list_team)

    @button(label='Créer', style=ButtonStyle.primary,emoji="🆕")
    async def make_team(self,button,interaction):

        await interaction.response.send_modal(TeamModal(self,self.team_members.values))