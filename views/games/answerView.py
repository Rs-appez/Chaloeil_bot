from nextcord.enums import ButtonStyle
from nextcord.ui import View , Button

class AnswerView(View):

    class ButtonAnswer(Button):

        def __init__(self,answer):
            self.answer = answer

            super().__init__(label=answer,style=ButtonStyle.primary)

        async def callback(self,interaction):
            
            player = [p for p in self.view.game.players if p.member.id == interaction.user.id]

            if player :
                await interaction.response.send_message(content=f"Tu as répondu : \"_{self.answer}_\"",ephemeral=True)
                await self.view.game.set_player_answer(player[0],self.answer)
                
            else :
                await interaction.response.send_message(content=f"https://tenor.com/view/the-sixth-sense-haley-joel-osment-cole-sear-i-see-dead-people-dead-gif-4431095",ephemeral=True)

    def __init__(self,game,question):

        self.question = question
        self.game = game
        super().__init__()
        for answer in question.get_answers():

            self.add_item(self.ButtonAnswer(answer))
