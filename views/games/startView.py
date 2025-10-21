from nextcord import ButtonStyle
from nextcord.ui import View, button
import asyncio


class StartView(View):
    def __init__(self, game) -> None:
        super().__init__(timeout=None)

        self.game = game

    @button(label="START !", style=ButtonStyle.primary)
    async def start(self, button, interaction):
        if interaction.user.id == self.game.creator_id:
            button.disabled = True
            await interaction.response.edit_message(view=self)
            asyncio.create_task(self.game.start())

        else:
            await interaction.response.send_message(
                "Seul celui qui a démarré le jeu peut le lancer.", ephemeral=True
            )

