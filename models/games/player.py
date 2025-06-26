from nextcord import Member


class Player:
    def __init__(self, member: Member, life_point=3, points=0) -> None:
        self.member = member
        self.dm_chan = None
        self.life_point = life_point
        self.points = points

    def __str__(self) -> str:
        if self.member.nick:
            return self.member.nick
        else:
            return self.member.name

    async def dm(self, msg, view=None):
        if not self.dm_chan:
            self.dm_chan = await self.member.create_dm()
        await self.dm_chan.send(msg, view=view)

    def loose_life_point(self, loose=1):
        self.life_point = self.life_point - loose

        if self.life_point < 0:
            self.life_point = 0

        return self.life_point

    def add_life_point(self, add=1):
        self.life_point = self.life_point + add

        return self.life_point

    def loose_point(self, loose=1, negative=True):
        self.points = self.points - loose

        if self.points < 0 and not negative:
            self.points = 0

        return self.life_point

    def add_point(self, add=1):
        self.points = self.points + add

        return self.life_point


class Team(Player):
    def __init__(self, members, name, life_point=3, points=0) -> None:
        super().__init__(None, life_point, points)

        self.members = members
        self.name = name

    def __str__(self) -> str:
        string = f"**{self.name}** ( "
        for member in self.members:
            string += f"{member}, "
        return string[:-2] + " )"

    async def dm(self, msg, view=None):
        return
