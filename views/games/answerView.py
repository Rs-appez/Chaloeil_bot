from nextcord.enums import ButtonStyle
from nextcord.ui import View , Button

class AnswerView(View):

    class ButtonAnswer(Button):

        def __init__(self,answer):
            self.answer = answer

            super().__init__(label=answer,style=ButtonStyle.primary)

        async def callback(self,interaction):
            
            player = [p for p in self.view.game.players if p.member.id == interaction.user.id][0]
            await self.view.game.set_player_answer(player,self.answer)
            await interaction.response.send_message(content=f"Tu as répondu : \"_{self.answer}_\"",ephemeral=True)
    
    def __init__(self,game,question):

        self.question = question
        self.game = game
        super().__init__()
        for answer in question.get_answers():

            self.add_item(self.ButtonAnswer(answer))
