from models.games.question import Question


class BattleRoyal():

    def __init__(self) -> None:
        self.questions = self.__get_questions()

    
    def __get_questions(self):

        return [Question.get_questions()]

    async def start(self,ch):
        await ch.send(self.questions[0].answer.show_answers())
