from models.games.quizz import Quizz


class BattleRoyal(Quizz):

    def __init__(self, channel, creator_id, category, team = False) -> None:
        super().__init__(channel, creator_id, category, team=team)
        
        self.statement_string = f"Bienvenue dans le grand quiz du Chaloeil !\n\nVous allez devoir répondre à une série de {self.nb_question} questions.\nVous partez à 3 points de vie.\nNe pas répondre correctement à une question vous fait perdre 1 point de vie.\n\n**__Règles__** :\n\n> 1 minute par question\n> fin de la question si tous les joueurs ont répondu\n> vous pouvez changer de réponse tant que tous les joueurs n'ont pas répondu\n> si tous les joueurs meurent en même temps, le round est annulé."
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

        return players
    
    def _display_player(self, res_string,players):
        res_string += "\n__Joueur encore dans la course :__\n"
        players = sorted(players,key=lambda p: p.life_point,reverse=True)
        
        for player in players:

            res_string += f"{player} : {player.life_point} pdv\n"
        
        return res_string

    def _check_winner(self,players):
        if len(players) == 1:
            return True
        return False
