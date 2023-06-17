from models.games.player import Player
from models.games.question import Question
from views.games.answerView import AnswerView
import config

class BattleRoyal():

    def __init__(self, channel) -> None:
        self.questions = self.__get_questions()
        self.channel = channel
        self.players = []
    
    def __get_questions(self):

        return [Question.get_questions()]

    async def start(self):
        await self.__init_players()
        print(self.players)

    async def show_question(self,question : Question):
        await self.channel.send(question.question,view=AnswerView(question))


    async def __init_players(self):
        for player in await self.channel.fetch_members():
            if not player.id == int(config.CHALOEIL_ID):
                self.players.append((Player(await player.fetch_member()),3))

