from .quizz import Quizz
from .question import Question


class QuestionsOfTheDay(Quizz):
    def __init__(self, channel, creator_id, time_to_answer=30) -> None:
        super().__init__(
            channel,
            creator_id,
            category=None,
            team=False,
            time_to_answer=time_to_answer,
        )
        self.statement_string = (
            f"Bienvenue dans le QOTD !\n\nVous allez devoir répondre à une question du jour.\n\n"
            f"**__Règles__** :\n\n> {self.time_to_answer} secondes pour répondre\n> Fin de la question si tous les joueurs ont répondu\n"
            "> Vous pouvez changer de réponse tant que tous les joueurs n'ont pas répondu"
            "\n\n**__Points__** :\n\n> 1 point par bonne réponse\n> 0 point par mauvaise réponse\n\n"
        )

    def _get_question(self) -> Question:
        if self.questions is None:
            self.questions = Question.get_questions_of_the_day()

        return self.questions.pop(0) if self.questions else None
