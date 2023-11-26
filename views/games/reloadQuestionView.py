from nextcord import ButtonStyle
from nextcord.ui import View, button

class ReloadQuestionView(View):

    def __init__(self,game) -> None:
        super().__init__()

        self.game = game

    @button(label='Recharger', style=ButtonStyle.primary,emoji="🔄")
    async def statement(self,button,interaction):

        button.disabled = True
        await interaction.response.edit_message(view=self)
        await self.game.show_question()
