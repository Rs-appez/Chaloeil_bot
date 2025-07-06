from .quizz import Quizz
from .question import Question


class QuestionsOfTheDay(Quizz):
    def __init__(self, channel, creator_id, time_to_answer=30) -> None:
        super().__init__(
            channel,
            creator_id,
            category=None,
            time_to_answer=time_to_answer,
        )
        self.__init_question()
        self.statement_string = (
            f"Bienvenue dans le **Quizz du jour!**\n\nVous allez devoir répondre à la série de questions sélectionnées pour aujourd'hui."
            f" *({self.nb_question} questions)*\n"
            "Une fois le Quizz commencé, il n'y aura pas de pause possible avant la fin de la série.\n\n"
            f"**__Règles__** :\n\n> {self.time_to_answer} secondes par question\n> Tous les participants ont la même série *(dans le même ordre)*\n"
            "> **__Il est strictement interdit de communiquer les questions ou les réponses avec quiconque__ !!!**\n"
            "> **__Il est strictement interdit de s'aider de n'importe quelle aide durant le Quizz__ !!!**\n"
            "\n\n**__Points__** :\n\n"
            f"> {self.difficulty_point['Easy']} point par question **Easy**\n> {self.difficulty_point['Medium']} points par question **Medium**\n> {self.difficulty_point['Hard']} points par question **Hard**\n> {self.difficulty_point['HARDCORE']} points par question **HARDCORE**\n> 0 point par mauvaise réponse\n\n"
            "\nUne fois fois avoir lu et compris ces règles, vous pouvez commencer le Quizz en cliquant sur le bouton ci-dessous.\n"
            "<:chaloeil:1386369580275994775> Bonne chance ! <:chaloeil:1386369580275994775>\n\n"
        )

    def __init_question(self) -> None:
        self.questions = Question.get_questions_of_the_day()
        self.nb_question = len(self.questions)

    def _get_question(self) -> Question:
        return self.questions.pop(0) if self.questions else None

    async def _display_winner(self, players) -> None:
        msg = f"Vous avez terminé le Quizz du jour avec un score de **{players[0].points}** points !\n"
        await self.channel.send(msg)
