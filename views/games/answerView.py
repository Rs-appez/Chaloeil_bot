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
                player = [
                    p
                    for p in self.view.game.players
                    if p.member.id == interaction.user.id
                ]

                if self.view.game.team and player:
                    player = [
                        t for t in self.view.game.teams if player[0] in t.members]

                if player:
                    await interaction.response.send_message(
                        content=f'Tu as répondu : "_{self.answer}_"', ephemeral=True
                    )
                    self.view.game.set_player_answer(player[0], self.answer)

                else:
                    await interaction.response.send_message(
                        content="https://tenor.com/view/the-sixth-sense-haley-joel-osment-cole-sear-i-see-dead-people-dead-gif-4431095",
                        ephemeral=True,
                    )

    def __init__(self, question, game=None):
        self.game = game
        super().__init__(timeout=None)
        for answer in question.get_answers():
            self.add_item(self.ButtonAnswer(answer))

    async def disable_all(self):
        self.stop()

        for child in self.children:
            child.disabled = True

        await self.game.answer_msg.edit(view=self)
