from models.exceptions import LogException
import config
import httpx
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

    _client = None

    @classmethod
    async def get_client(cls):
        if cls._client is None:
            cls._client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        return cls._client

    @classmethod
    async def close_client(cls):
        if cls._client is not None:
            await cls._client.aclose()
            cls._client = None

    @staticmethod
    async def init_players(players: List[Player]) -> bool:
        """Initialize player statistics in the backend."""

        print("url stat : ", Statisics.stats_url)
        client = await Question.get_client()
        player_ids = [
            {"discord_id": str(player.member.id), "name": player.member.name}
            for player in players
        ]
        data = {"players": json.dumps(player_ids)}

        response = await client.post(
            Statisics.stats_url + "players/add_players/",
            json=data,
            headers=Statisics.headers,
        )

        return response.status_code == 201

    @staticmethod
    async def init_teams(teams: List[Team]) -> bool:
        """Initialize team statistics in the backend."""

        client = await Question.get_client()
        team_data = [
            {
                "name": team.name,
                "players": [str(member.member.id) for member in team.members],
            }
            for team in teams
        ]
        data = {"teams": json.dumps(team_data)}

        response = await client.post(
            Statisics.stats_url + "teams/add_teams/",
            json=data,
            headers=Statisics.headers,
        )

        return response.status_code == 201

    @staticmethod
    async def send_answers(
        players: List[tuple[Player, Answer]], question: Question
    ) -> bool:
        """Send players's answer to the backend."""
        client = await Question.get_client()

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

        response = await client.post(
            Statisics.stats_url + "statistics/add_answer/",
            json=data,
            headers=Statisics.headers,
        )

        return response.status_code == 201

    @staticmethod
    async def send_score(player: Player) -> bool:
        """Send player's score to the backend."""
        client = await Question.get_client()

        data = {
            "player_id": player.member.id,
            "score": player.points,
        }

        response = await client.post(
            Statisics.stats_url + "qotdStatistics/add_score/",
            json=data,
            headers=Statisics.headers,
        )
        if response.status_code == 200:
            return True

        return False

    @staticmethod
    async def log_player_participation(player: Player, qotd_id: int):
        client = await Question.get_client()

        """Log player's participation to the backend."""
        data = {
            "player_id": player.member.id,
            "qotd_id": qotd_id,
        }

        response = await client.post(
            Statisics.stats_url + "qotdStatistics/log_player/",
            json=data,
            headers=Statisics.headers,
        )

        if response.status_code == 403:
            raise LogException("Vous avez déjà participé au Quizz du jour aujourd'hui.")

        if response.status_code != 201:
            raise Exception(
                "Une erreur est survenue lors de l'enregistrement de votre participation au Quizz du jour. Veuillez réessayer plus tard."
            )
