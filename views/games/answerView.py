from nextcord.enums import ButtonStyle
from nextcord.ui import View , Button

class AnswerView(View):

    class ButtonAnswer(Button):

        def __init__(self,answer):
            self.answer = answer
            # self.current_view = current_view

            super().__init__(label=answer,style=ButtonStyle.primary)

        async def callback(self,interaction):


            for btn in self.view.children:
                btn.disabled = True

            await interaction.response.edit_message(view=self.view)
    
    def __init__(self,question):

        self.question = question
        super().__init__(timeout=60)
        for answer in question.get_answers():

            self.add_item(self.ButtonAnswer(answer))
