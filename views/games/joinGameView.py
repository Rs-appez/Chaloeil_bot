from nextcord.enums import ButtonStyle
from nextcord.ui import View , Button

class JoinGameView(View):

    class JoinButton(Button):

        def __init__(self,emoji):

            super().__init__(label="Participer",style=ButtonStyle.blurple,emoji=emoji)

        async def callback(self,interaction):

            await interaction.response.send_message(f"joined",ephemeral=True)

    def __init__(self,game,emoji) -> None:
        super().__init__(timeout=None)

        self.game = game
        self.emoji = emoji

        self.add_item(self.JoinButton(emoji))

