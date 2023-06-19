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
        self.current_question = None

    def __get_questions(self):

        return [Question.get_questions()]
    
    async def launch_statement(self):
        await self.channel.send("blabla\nblablabla",view=StartView(self))

    async def start(self):
        await self.__init_players()
        await self.show_question(self.questions[0])

    async def show_question(self,question : Question):
        self.current_question = question
        await self.channel.send(question.question,view=AnswerView(self,question))


    async def __init_players(self):
        for player in await self.channel.fetch_members():
            if not player.id == int(config.CHALOEIL_ID):
                self.players.append(Player(await player.fetch_member()))

    async def set_player_answer(self,player : Player, answer : str):

        if player in [p[0] for p in self.player_answer] :
                
            self.player_answer.remove([p for p in self.player_answer if p[0] == player][0])

        self.player_answer.append((player,answer))

        if len(self.players) == len(self.player_answer):
            await self.check_result()

    async def check_result(self):
        res_string = f"La réponse était : **{self.current_question.get_answer()}**\n\n__Joueur encore dans la course :__\n"

        for player in self.players:
            player_answer = [pa[1] for pa in self.player_answer if pa[0] == player]
            if not player_answer or  not self.current_question.check_answer(player_answer[0]):
                player.loose_life_point()
            res_string += f"{player} : {player.life_point} pdv\n"
        
        self.player_answer = []
        await self.channel.send(res_string)