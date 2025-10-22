from models.games.player import Player
from .quizz import Quizz
from .question import Question
from models.statistics.stats import Statisics


class QuestionsOfTheDay(Quizz):
    def __init__(self, channel, creator_id, time_to_answer=30) -> None:
        super().__init__(
            channel,
            creator_id,
            category=None,
            time_to_answer=time_to_answer,
        )
        self.qotd_id: int = None
        self.statement_string = (
            f"Bienvenue dans le **Quizz du jour!**\n\nVous allez devoir répondre à la série de questions sélectionnées pour aujourd'hui."
            f" *({self.nb_question} questions)*\n"
            "Une fois le Quizz commencé, il n'y aura pas de pause possible avant la fin de la série.\n\n"
            f"**__Règles__** :\n\n> {
                self.time_to_answer
            } secondes par question\n> Tous les participants ont la même série *(dans le même ordre)*\n"
            "> **__Il est strictement interdit de communiquer les questions ou les réponses avec quiconque__ !!!**\n"
            "> **__Il est strictement interdit de s'aider de n'importe quelle aide durant le Quizz__ !!!**\n"
            "\n\n**__Points__** :\n\n"
            f"> {self.difficulty_point['Easy']} point par question **Easy**\n> {
                self.difficulty_point['Medium']
            } points par question **Medium**\n> {
                self.difficulty_point['Hard']
            } points par question **Hard**\n> {
                self.difficulty_point['HARDCORE']
            } points par question **HARDCORE**\n> 0 point par mauvaise réponse\n\n"
            "\nUne fois fois avoir lu et compris ces règles, vous pouvez commencer le Quizz en cliquant sur le bouton ci-dessous.\n"
            "<:chaloeil:1386369580275994775> Bonne chance ! <:chaloeil:1386369580275994775>\n\n"
        )

    @classmethod
    async def create(
        cls, channel, creator_id, time_to_answer=30
    ) -> "QuestionsOfTheDay":
        self = cls(channel, creator_id, time_to_answer)
        await self.__init_question()
        return self

    async def _init_players(self) -> None:
        await super()._init_players()
        await Statisics.log_player_participation(self.players[0], self.qotd_id)

    async def __init_question(self) -> None:
        qotd = await Question.get_questions_of_the_day(self.creator_id)
        if not qotd:
            raise ValueError("No questions available for the day.")

        self.questions, self.qotd_id = qotd
        self.nb_question = len(self.questions)

    async def _get_question(self) -> Question:
        return self.questions.pop(0) if self.questions else None

    async def _display_winner(self, players) -> None:
        player = players[0]
        await Statisics.send_score(player)
        msg = f"Vous avez terminé le Quizz du jour avec un score de **{
            player.points
        }** points !\n"
        await self.channel.send(msg)
