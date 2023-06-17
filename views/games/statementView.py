from nextcord import ButtonStyle
from nextcord.ui import View, button

class StatementView(View):

    def __init__(self,game) -> None:
        super().__init__(timeout=None)

        self.game = game

    @button(style=ButtonStyle.primary,emoji="📜")
    async def statement(self,button,interaction):

        button.disabled = True
        await interaction.response.edit_message(view=self)
        await self.game.launch_statement()
