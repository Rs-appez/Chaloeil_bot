import asyncio
from models.games.timer import Timer
from models.games.player import Player
from models.games.team import Team
from models.games.question import Question
from views.games.answerView import AnswerView
import config
from views.games.createTeamView import CreateTeamView
from views.games.reloadQuestionView import ReloadQuestionView
from views.games.startView import StartView

class Quizz():

    def __init__(self, channel, creator_id, category, nb_question = 1, team = False) -> None:
        self.channel = channel
        self.creator_id = creator_id
        self.category = category
        self.nb_question = nb_question
        self.team = team
        self.players = []
        self.teams = []
        self.player_answer = []
        self.current_question = None
        self.timer = None

        self.statement_string = "blabla\nblablabla"
        self.questions = None

    def _get_question(self):
        if self.questions is None or len(self.questions) == 0 :
            self.questions = Question.get_question(self.nb_question,cat=self.category)

        return self.questions.pop(0)

    async def launch_statement(self):
        await self.channel.send(self.statement_string,view=StartView(self))

    async def start(self):
        await self.__init_players()

        if self.team :
            await self.__init_teams()
        else :
            await self.show_question()

    async def show_question(self):
        print(self.teams)
        self.current_question = self._get_question()
        if self.current_question is None:
            await self.channel.send("Erreur lors de la récupération de la question 😭",view=ReloadQuestionView(self))
            return
        question_msg = "‎ ‎\n" +self.current_question.question
        if self.current_question.image_url :
            await self.channel.send(self.current_question.image_url)
        await self.channel.send(question_msg,view=AnswerView(self,self.current_question))

        self.timer = Timer(40, self.check_result,asyncio.get_running_loop())


    async def __init_players(self):
        for player in await self.channel.fetch_members():
            if not player.id == int(config.CHALOEIL_ID):
                self.players.append(Player(await player.fetch_member()))
    
    async def __init_teams(self):
        list_team_msg = await self.channel.send("Aucune équipe pour le moment")
        await self.channel.send("Crée ton équipe !",view=CreateTeamView(self,list_team_msg))

    async def add_team(self,team : Team):
        self.teams.append(team)
        

    async def set_player_answer(self,player : Player, answer : str):

        if player in [p[0] for p in self.player_answer] :
                
            self.player_answer.remove([p for p in self.player_answer if p[0] == player][0])

        self.player_answer.append((player,answer))

        if len(self.players) == len(self.player_answer):
            self.timer.stop()

    def _compute_score(self):
        
        for player in self.players:
            player_answer = [pa[1] for pa in self.player_answer if pa[0] == player]
            if len(player_answer) > 0 and self.current_question.check_answer(player_answer[0]):
                player.add_point()


    def _display_player(self, res_string):
        res_string += "\n__Classement des joueurs :__\n"
        for player in sorted(self.players,key=lambda p: p.points,reverse=True):

            res_string += f"{player} : {player.points} points !\n"
            
        return res_string

    async def check_result(self):

        self._compute_score()

        #Display result
        answers = self.current_question.get_good_answers()
        if len(answers) == 1:
            res_string = f"La réponse était : **{answers[0]}**\n"
        else :
            res_string = f"Les réponses étaient : **{', '.join(answers)}**\n"
            
        res_string = self._display_player(res_string)
            
        self.player_answer = []
        await self.channel.send(res_string)

        await self.__next_question()

    def _check_winner(self):
       return len(self.questions) == 0
    
    async def __next_question(self):
        if self._check_winner():
            await self.channel.send(f"\n**{self.players[0]} a gagné !**")
            await asyncio.sleep(10)
            await self.channel.send("💥  *Ce channel va s'autodétruire dans 60 secondes !* 💥")
            await self.channel.send("https://tenor.com/view/self-destruction-imminent-please-evacuate-gif-8912211")
            await asyncio.sleep(60)
            await self.self_destruct()
        else :
            await asyncio.sleep(8)
            await self.show_question()

    async def self_destruct(self):
        await self.channel.delete()