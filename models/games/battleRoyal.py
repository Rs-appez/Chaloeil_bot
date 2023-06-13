from models.games.question import Question


class BattleRoyal():

    def __init__(self) -> None:
        self.questions = self.__get_question()

    
    def __get_questions(self):

        return [Question.get_questions()]