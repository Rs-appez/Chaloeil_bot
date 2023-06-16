from models.games.question import Question
from views.games.answerView import AnswerView


class BattleRoyal():

    def __init__(self, channel) -> None:
        self.questions = self.__get_questions()
        self.channel = channel

    
    def __get_questions(self):

        return [Question.get_questions()]

    async def start(self):
        await self.show_question(self.questions[0])


    async def show_question(self,question : Question):
        await self.channel.send(question.question,view=AnswerView(question))
