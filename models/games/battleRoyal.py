from models.games.quizz import Quizz
from models.games.player import Player

import config
from models.games.player import Team


class BattleRoyal(Quizz):
    def __init__(
        self,
        channel,
        creator_id,
        category,
        team=False,
        life_point=3,
        keep=False,
        debug=False,
        time_to_answer=30,
    ) -> None:
        super().__init__(
            channel,
            creator_id,
            category,
            team=team,
            keep=keep,
            debug=debug,
            time_to_answer=time_to_answer,
        )
        self.life_point = life_point

        self.statement_string = (
            f"Bienvenue dans le grand quiz du Chaloeil !\n\nVous allez devoir répondre à une série de questions.\nVous partez à {self.life_point} points de vie.\n"
            f"Ne pas répondre correctement à une question vous fait perdre 1 point de vie.\n\n**__Règles__** :\n\n> {self.time_to_answer} secondes par question\n"
            "> fin de la question si tous les joueurs ont répondu\n> vous pouvez changer de réponse tant que tous les joueurs n'ont pas répondu\n"
            "> si tous les joueurs meurent en même temps, le round est annulé."
        )

    async def show_question(self, altenative_sentence=None):
        await super().show_question("")

    async def _init_players(self):
        for player in await self.channel.fetch_members():
            if not player.id == int(config.CHALOEIL_ID):
                self.players.append(
                    Player(await player.fetch_member(), life_point=self.life_point)
                )

    def _compute_score(self, players):
        for player in players:
            player_answer = [pa[1]
                             for pa in self.player_answer if pa[0] == player]
            if not player_answer or not player_answer[0]:
                player.loose_life_point()

        players_in_life = [p for p in players if p.life_point > 0]

        if len(players_in_life) > 0:
            players = players_in_life
        else:
            for player in players:
                player.add_life_point()

        return players

    def make_team(self, team_members, team_name) -> Team:
        return Team(team_members, team_name, life_point=self.life_point)

    def _display_player(self, res_string, players):
        res_string += "\n__Joueur encore dans la course :__\n"
        players = sorted(players, key=lambda p: p.life_point, reverse=True)

        for player in players:
            res_string += f"{player} : {player.life_point} pdv\n"

        return res_string

    def _check_winner(self, players):
        if len(players) == 1:
            return True
        return False
