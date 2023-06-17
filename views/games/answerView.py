from nextcord.enums import ButtonStyle
from nextcord.ui import View , Button

class AnswerView(View):

    class ButtonAnswer(Button):

        def __init__(self,answer):
            self.answer = answer

            super().__init__(label=answer,style=ButtonStyle.primary)

        async def callback(self,interaction):


            # for btn in self.view.children:
            #     btn.disabled = True

            await interaction.response.send_message(f"{self.view.question.check_answer(self.answer)}",ephemeral=True)
    
    def __init__(self,question):

        self.question = question
        super().__init__()
        for answer in question.get_answers():

            self.add_item(self.ButtonAnswer(answer))
