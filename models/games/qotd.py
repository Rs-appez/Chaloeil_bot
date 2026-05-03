import asyncio
from typing import override

from views.games.chooseCategoryView import ChooseCategoryView
from .quizz import Quizz
from .question import Question
from models.statistics.stats import Statisics
from views.games.startView import StartView


class QuestionsOfTheDay(Quizz):
    def __init__(self, channel, creator_id, time_to_answer=25) -> None:
        super().__init__(
            channel,
            creator_id,
            category=None,
            time_to_answer=time_to_answer,
        )
        self.qotd_id: int | None = None
        self.ask_final_question: bool = False

    @classmethod
    async def create(
        cls, channel, creator_id, time_to_answer=25
    ) -> "QuestionsOfTheDay":
        self = cls(channel, creator_id, time_to_answer)
        await self.__init_question()
        return self

    @override
    async def launch_statement(self):
        statement_string = (
            f"Bienvenue dans le **Quizz du jour!**\n\nVous allez devoir répondre à la série de questions sélectionnées pour aujourd'hui."
            f" *({self.nb_question + 1} questions)*\n"
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
        _ = await self.channel.send(statement_string, view=StartView(self))

    @override
    async def _init_players(self) -> None:
        if not self.qotd_id:
            raise ValueError("QOTD ID must be set before initializing players.")
        await super()._init_players()
        await Statisics.log_player_participation(self.players[0], self.qotd_id)

    async def __init_question(self) -> None:
        qotd = await Question.get_questions_of_the_day(self.creator_id)
        if not qotd:
            raise ValueError("No questions available for the day.")

        self.questions, self.qotd_id = qotd
        self.nb_question = len(self.questions)

    @override
    async def _get_question(self) -> Question | None:
        return self.questions.pop(0) if self.questions else None

    @override
    def _check_winner(self, players) -> bool:

        if self.questions and len(self.questions) > 0:
            return False
        elif not self.ask_final_question:
            self.ask_final_question = True
            return False
        return True

    @override
    async def _next_question(self, players):
        if self._check_winner(players):
            await self._display_winner(players)
            await self._clear_channel()
        elif self.ask_final_question:
            await self.__ask_final_question()
        else:
            await asyncio.sleep(5)
            await self.show_question()

    async def __ask_final_question(self):
        _ = await self.channel.send(
            content=(
                "**Dernière question !**\nMais je vais etre sympa, "
                "je vais vous laisser choisir la catégorie de la question finale !\n"
                "Choisissez la catégorie qui vous portera chance ci-dessous"
            ),
            view=ChooseCategoryView(self),
        )

    async def load_final_question(self, category):
        last_question = await Question.create_standalone_qotd(category)
        if not last_question:
            raise ValueError("No question found for the final question.")

        self.questions = [last_question]
        await self.show_question(
            altenative_sentence="## Voici la question que j'ai sélectionnée rien que pour toi !"
        )

    @override
    async def _display_winner(self, players) -> None:
        player = players[0]
        _ = asyncio.create_task(Statisics.send_score(player))
        msg = f"Vous avez terminé le Quizz du jour avec un score de **{
            player.points
        }** points !\n"
        _ = await self.channel.send(msg)
