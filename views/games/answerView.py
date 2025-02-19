from nextcord.ui import View, Button
from nextcord.enums import ButtonStyle


class AnswerView(View):
    class ButtonAnswer(Button):
        def __init__(self, answer):
            self.answer = answer.answer_text

            super().__init__(
                label=self.answer, style=ButtonStyle.primary, emoji=answer.emoji
            )

        async def callback(self, interaction):
            if self.view.game:
                await self.view._answer_for_game(interaction, self.answer)

            elif self.view.player:
                await self.view._answer_for_player(interaction, self.answer)

    def __init__(self, question, game=None, player=None):
        self.game = game
        self.player = player
        self.question = question

        super().__init__(timeout=None)
        for answer in self.question.get_answers():
            self.add_item(self.ButtonAnswer(answer))

    async def disable_all(self):
        self.stop()

        for child in self.children:
            child.disabled = True

        await self.game.answer_msg.edit(view=self)

    async def _answer_for_game(self, interaction, answer):
        player = [
            p for p in self.game.players if p.member.id == interaction.user.id
        ]

        if self.game.team and player:
            player = [t for t in self.game.teams if player[0] in t.members]

        if player:
            await interaction.response.send_message(
                content=f'Tu as répondu : "_{answer}_"', ephemeral=True
            )
            self.game.set_player_answer(player[0], answer)

        else:
            await interaction.response.send_message(
                content="https://tenor.com/view/the-sixth-sense-haley-joel-osment-cole-sear-i-see-dead-people-dead-gif-4431095",
                ephemeral=True,
            )

    async def _answer_for_player(self, interaction, answer):
        if self.player.id == interaction.user.id:
            username = self.player.nick or self.player.name

            message = f'**{username}** as répondu : "_{answer}_"\n'

            if self.question.check_answer(answer):
                message += "C'est **la bonne** réponse !"
            else:
                message += "Ce **n'est pas la bonne** réponse 😭"

            await interaction.response.send_message(
                content=message
            )

        else:
            await interaction.response.send_message(
                content="Seulement la personne interrogée peut répondre à la question",
                ephemeral=True,
            )
