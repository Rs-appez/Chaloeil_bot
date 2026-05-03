from random import shuffle
from models.games.player import Player
import math


class TeamMaker:
    def __init__(self, team_size, players: set[Player]) -> None:
        self.team_size = team_size
        self.__players: list[Player] = list(players)
        self.__teams: list[list[Player]] = []
        self.__old_teams: set[frozenset[Player]] = set()
        self.__max_teams = math.comb(len(players), team_size)

    @property
    def teams(self) -> list[list[Player]]:
        return self.__teams

    def make_teams(self) -> list[list[Player]]:
        if len(self.__old_teams) >= self.__max_teams:
            self.__old_teams.clear()
        self.__teams = []
        players_copy = self.__players[:]
        while len(players_copy) >= self.team_size:
            max_attempts = 1000
            for _ in range(max_attempts):
                shuffle(players_copy)
                team = players_copy[: self.team_size]
                team_set = frozenset(team)
                if team_set not in self.__old_teams:
                    self.__teams.append(team)
                    self.__old_teams.add(team_set)
                    players_copy = players_copy[self.team_size :]
                    break
            else:
                # No unique combination found, reset history and retry
                self.__old_teams.clear()

        return self.teams


if __name__ == "__main__":
    print("Test de TeamMaker")
    players = [Player(None) for _ in range(6)]
    team_maker = TeamMaker(2, players)
    for _ in range(10):
        teams = team_maker.make_teams()
        for i, team in enumerate(teams):
            print(f"Team {i + 1}: {[p for p in team]}")
        print("-" * 20)
