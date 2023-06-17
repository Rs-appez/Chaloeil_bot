from nextcord import ButtonStyle
from nextcord.ui import View, button

class StartView(View):

    def __init__(self,game) -> None:
        super().__init__(timeout=None)

        self.game = game

    @button(label="START !",style=ButtonStyle.primary)
    async def start(self,button,interaction):

        button.disabled = True
        await interaction.response.edit_message(view=self)
        await self.game.start()
