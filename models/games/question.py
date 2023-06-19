from models.games.answer import Answer


class Question():

    def __init__(self, question, answer, level , cat) -> None:
        self.question = question
        self.answer = answer
        self.level = level
        self.cat = cat

    @staticmethod
    def get_questions(level = None, cat = None):

        return Question("pourquoi",Answer("42",["21","la reponse D","parceque"]),0,"test")
    
    def get_answers(self):

        return self.answer.show_answers()
        
    def get_answer(self) -> str:

        return self.answer.good_answer
    
    def check_answer(self,answer):

        return self.answer.check_answer(answer)
