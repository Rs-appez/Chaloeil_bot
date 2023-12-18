from models.games.question import Question
from models.games.quizz import Quizz


class BattleRoyal(Quizz):

    def __init__(self, channel, creator_id, category) -> None:
        super().__init__(channel, creator_id, category)
        
        self.statement_string = "battle !!!\nblablabla"

    def _get_question(self):

        return Question.get_question(self.nb_question ,cat=self.category)

    def _compute_score(self,players):

        for player in players:
            player_answer = [pa[1] for pa in self.player_answer if pa[0] == player]
            if not player_answer or  not self.current_question.check_answer(player_answer[0]):
                player.loose_life_point()

        players_in_life = [p for p in players if p.life_point > 0]

        if len(players_in_life) > 0:
            players = players_in_life
        else :
            for player in self.players:
                player.add_life_point()

    def _display_player(self, res_string,players):
        res_string += "\n__Joueur encore dans la course :__\n"
        for player in sorted(players,key=lambda p: p.life_point,reverse=True):

            res_string += f"{player} : {player.life_point} pdv\n"
        
        return res_string

    def _check_winner(self,players):
        if len(players) == 1:
            return True
        return False
