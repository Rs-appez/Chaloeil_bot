
from models.games.player import Player

class Team(Player):

    def __init__(self, members ,name, life_point=3, points=0) -> None:
        super().__init__(None, life_point, points)

        self.members = members
        self.name = name

    def __str__(self) -> str:
        string = f"**{self.name}** ( "
        for member in self.members:
            if member.nick :
                string += f"{member.nick}, "
            else :
                string += f"{member.name}, "

        return string[:-2] + " )"
        
    async def dm(self,msg,view = None):
        return