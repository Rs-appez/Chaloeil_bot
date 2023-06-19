from nextcord import Member

class Player():

    def __init__(self,member : Member, life_point = 3 ) -> None:
        self.member = member
        self.dm_chan = None
        self.life_point = life_point

    def __str__(self) -> str:
        if self.member.nick :
            return self.member.nick
        else :
            return self.member.name
        
    async def dm(self,msg,view = None):
        if not self.dm_chan :
            self.dm_chan = await self.member.create_dm()
        await self.dm_chan.send(msg,view=view)

    def loose_life_point(self,loose = 1):

        self.life_point = self.life_point - loose

        if self.life_point < 0 :
            self.life_point = 0
        
        return self.life_point