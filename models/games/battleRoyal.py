from models.games.player import Player
from models.games.question import Question
from views.games.answerView import AnswerView
import config
from views.games.startView import StartView

class BattleRoyal():

    def __init__(self, channel, creator_id) -> None:
        self.questions = self.__get_questions()
        self.channel = channel
        self.creator_id = creator_id
        self.players = []
        self.player_answer = []

    def __get_questions(self):

        return [Question.get_questions()]
    
    async def launch_statement(self):
        await self.channel.send("blabla\nblablabla",view=StartView(self))

    async def start(self):
        await self.__init_players()
        await self.show_question(self.questions[0])

    async def show_question(self,question : Question):
        await self.channel.send(question.question,view=AnswerView(self,question))


    async def __init_players(self):
        for player in await self.channel.fetch_members():
            if not player.id == int(config.CHALOEIL_ID):
                self.players.append(Player(await player.fetch_member()))

    def set_player_answer(self,player : Player, answer : str):

        if player in [p[0] for p in self.player_answer] :
                
            self.player_answer.remove([p for p in self.player_answer if p[0] == player][0])

        self.player_answer.append((player,answer))

        print(self.player_answer)

