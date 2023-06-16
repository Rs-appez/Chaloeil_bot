from nextcord import Member

class Player():

    def __init__(self,member : Member) -> None:
        self.member = member
        self.dm_chan = None

    def __str__(self) -> str:
        return self.member.nick
    
    async def dm(self,msg,view = None):
        if not self.dm_chan :
            self.dm_chan = await self.member.create_dm()
        await self.dm_chan.send(msg,view=view)