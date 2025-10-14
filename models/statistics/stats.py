from models.exceptions import LogException
import config
import requests
from requests.models import Response
import json
from typing import List

from models.games.player import Player, Team
from models.games.question import Question, Answer


class Statisics:
    stats_url = config.BACKEND_URL + "statistics/api/"

    headers = {
        "Authorization": config.BACKEND_TOKEN,
        "Content-Type": "application/json",
    }

    @staticmethod
    def init_players(players: List[Player]) -> bool:
        """Initialize player statistics in the backend."""

        player_ids = [
            {"discord_id": str(player.member.id), "name": player.member.name}
            for player in players
        ]
        data = {"players": json.dumps(player_ids)}

        response = requests.post(
            Statisics.stats_url + "players/add_players/",
            json=data,
            headers=Statisics.headers,
        )

        return response.status_code == 201

    @staticmethod
    def init_teams(teams: List[Team]) -> bool:
        """Initialize team statistics in the backend."""

        team_data = [
            {
                "name": team.name,
                "players": [str(member.member.id) for member in team.members],
            }
            for team in teams
        ]
        data = {"teams": json.dumps(team_data)}

        response = requests.post(
            Statisics.stats_url + "teams/add_teams/",
            json=data,
            headers=Statisics.headers,
        )

        return response.status_code == 201

    @staticmethod
    def send_answers(players: List[tuple[Player, Answer]], question: Question) -> bool:
        """Send players's answer to the backend."""
        data = {
            "question_id": question.id,
            "answers": json.dumps(
                [
                    {
                        "player_id" if player.member else "players_id": str(
                            player.member.id
                        )
                        if player.member
                        else [str(p.member.id) for p in player],
                        "answer_id": answer.id if answer else -1,
                    }
                    for player, answer in players
                ]
            ),
        }

        response = requests.post(
            Statisics.stats_url + "statistics/add_answer/",
            json=data,
            headers=Statisics.headers,
        )

        return response.status_code == 201

    @staticmethod
    def send_score(player: Player) -> bool:
        """Send player's score to the backend."""
        data = {
            "player_id": player.member.id,
            "score": player.points,
        }

        response: Response = requests.post(
            Statisics.stats_url + "qotdStatistics/add_score/",
            json=data,
            headers=Statisics.headers,
        )
        if response.status_code == 200:
            return True

        return False

    @staticmethod
    def log_player_participation(player: Player, qotd_id: int):
        """Log player's participation to the backend."""
        data = {
            "player_id": player.member.id,
            "qotd_id": qotd_id,
        }

        response: Response = requests.post(
            Statisics.stats_url + "qotdStatistics/log_player/",
            json=data,
            headers=Statisics.headers,
        )

        if response.status_code == 403:
            print(response.json())
            raise LogException("Vous avez déjà participé au Quizz du jour aujourd'hui.")

        if response.status_code != 201:
            raise Exception(
                "Une erreur est survenue lors de l'enregistrement de votre participation au Quizz du jour. Veuillez réessayer plus tard."
            )
