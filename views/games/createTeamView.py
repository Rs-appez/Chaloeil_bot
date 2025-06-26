from nextcord import ButtonStyle
from nextcord.ui import View, button

from views.games.teamModal import TeamModal
from nextcord.ui import Select
from nextcord import SelectOption


class CreateTeamView(View):
    def __init__(self, game) -> None:
        super().__init__(timeout=None)

        self.game = game

    @button(label="Team", style=ButtonStyle.primary, emoji="🆕")
    async def make_team(self, button, interaction):
        await interaction.response.send_message(
            "*Selectione les membres de ton équipe dans le menu déroulant*",
            view=SelectPlayerView(self.game, interaction.user),
            ephemeral=True,
        )

    @button(label="START !", style=ButtonStyle.primary)
    async def start(self, button, interaction):
        if interaction.user.id == self.game.creator_id:
            for btn in self.children:
                btn.disabled = True
            await interaction.response.edit_message(view=self)
            await self.game.show_question()

        else:
            await interaction.response.send_message(
                "Seul celui qui a démarré le jeu peut le lancer", ephemeral=True
            )

    @button(label="Delete team", style=ButtonStyle.danger)
    async def delete_team(self, button, interaction):
        # interaction.user.id == self.game.creator_id or
        if interaction.user.id in [
            member.member.id for team in self.game.teams for member in team.members
        ]:
            for team in self.game.teams:
                if interaction.user.id in [member.member.id for member in team.members]:
                    self.game.remove_team(team)
                    await self.game.display_teams()
                    break

        else:
            await interaction.response.send_message(
                "Tu dois être dans une équipe pour pouvoir la supprimer", ephemeral=True
            )


class SelectPlayerView(View):
    def __init__(self, game, chief) -> None:
        super().__init__(timeout=None)

        self.game = game
        self.chief_user = chief

        self.team_name = None
        self.chief_player = [
            player for player in self.game.players if player.member.id == chief.id
        ][0]
        self.players = [
            player for player in self.game.players if player.member.id != chief.id
        ]

        self.players = [SelectOption(label=str(player))
                        for player in self.players]
        max_values = len(self.players) if len(self.players) < 4 else 4

        self.team_members = Select(
            placeholder="Team Members",
            min_values=1,
            max_values=max_values,
            options=self.players,
        )
        if len(self.players) != 0:
            self.add_item(self.team_members)

    async def add_team(self, team_name, team_members, interaction):
        team_members = [
            player for player in self.game.players if str(player) in team_members
        ]

        team = self.game.make_team(team_members, team_name)

        if not self.game.add_team(team):
            await interaction.response.send_message(
                "Certains joueurs sont déjà dans une équipe", ephemeral=True
            )
            return

        await self.game.display_teams()

    @button(label="Créer", style=ButtonStyle.primary, emoji="🆕")
    async def make_team(self, button, interaction):
        team = self.team_members.values
        if str(self.chief_player) not in team:
            team.insert(0, str(self.chief_player))
        await interaction.response.send_modal(TeamModal(self, team))

