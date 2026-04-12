from nextcord import ButtonStyle
from nextcord.ui import View, button

from models.games.question import Question


class FlagQuestionView(View):
    def __init__(self, admin_id: str, question: Question) -> None:
        super().__init__()

        self.admin_id = admin_id
        self.question = question

    @button(label="Réponse ou Question incorect", style=ButtonStyle.danger, emoji="⚠️")
    async def statement(self, button, interaction):

        if self.admin_id != interaction.user.id:
            await interaction.response.send_message(
                content="Seule la personne ayant démarré le quiz peut signaler une question ou une réponse comme étant incorrecte",
                ephemeral=True,
            )
            return

        button.disabled = True
        await interaction.response.edit_message(view=self)
        succes = await self.question.flag(interaction.user.id)
        if succes:
            await interaction.followup.send(
                content="Merci pour votre signalement, nous allons examiner la question et apporter les corrections nécessaires si besoin.",
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                content="Une erreur est survenue lors du signalement de la question. Veuillez le signaler à @Chaloeil.",
                ephemeral=True,
            )
