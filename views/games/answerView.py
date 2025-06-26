from nextcord.ui import View, Button
from nextcord.enums import ButtonStyle

from models.games.question import Answer

class AnswerView(View):
    class ButtonAnswer(Button):
        def __init__(self, answer: Answer):
            self.answer = answer

            super().__init__(
                label=self.answer.answer_text,
                style=ButtonStyle.primary,
                emoji=answer.emoji,
            )

        async def callback(self, interaction):
            if self.view.game:
                await self.view._answer_for_game(interaction, self.answer)

            elif self.view.player:
                if self.view.player.id == interaction.user.id:
                    if self.answer.is_correct:
                        self.style = ButtonStyle.green
                    else:
                        self.style = ButtonStyle.danger

                    await self.view._answer_for_player(interaction, self.answer)
                else:
                    await interaction.response.send_message(
                        content="Seulement la personne interrogée peut répondre à la question",
                        ephemeral=True,
                    )
            else:
                if self.answer.is_correct:
                    self.style = ButtonStyle.green
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

        if self.game:
            await self.game.answer_msg.edit(view=self)

    async def _answer_for_game(self, interaction, answer: Answer):
        player = [p for p in self.game.players if p.member.id ==
                  interaction.user.id]

        if self.game.team and player:
            player = [t for t in self.game.teams if player[0] in t.members]

        if player:
            await interaction.response.send_message(
                content=f'Tu as répondu : "_{answer.answer_text}_"', ephemeral=True
            )
            self.game.set_player_answer(player[0], answer)

        else:
            await interaction.response.send_message(
                content="https://tenor.com/view/the-sixth-sense-haley-joel-osment-cole-sear-i-see-dead-people-dead-gif-4431095",
                ephemeral=True,
            )

    async def _answer_for_player(self, interaction, answer: Answer):
        await self.disable_all()
        username = interaction.user.nick or interaction.user.name

        message = f'**{username}** as répondu : "_{answer.answer_text}_"\n'

        if answer.is_correct:
            message += "C'est **la bonne** réponse !"

        else:
            message += "Ce **n'est pas la bonne** réponse 😭\n"
            good_answers = self.question.get_good_answers()
            if len(good_answers) > 1:
                message += (
                    f"Les bonnes réponses étaient : || {', '.join(good_answers)} ||"
                )
            else:
                message += "La bonne réponse était :"
                if len(good_answers) > 0:
                    message += f" || {good_answers[0]} ||"

        await interaction.message.edit(view=self)
        await interaction.response.send_message(content=message)
