from nextcord.ui import Modal, TextInput
from nextcord import TextInputStyle

class SpeakModal(Modal):
    def __init__(self,bot, channel_id):
        super().__init__('Speak Modal')
        self.bot = bot

        self.channel_id = TextInput('Channel ID', placeholder='Channel ID',required=True, default_value=channel_id)
        self.msg = TextInput('Message', placeholder='Message',required=True, style=TextInputStyle.paragraph)

        self.add_item(self.msg)
        self.add_item(self.channel_id)

    async def callback(self, interaction):
        try:
            channel_id = int(self.channel_id.value)
            text_channel = self.bot.get_channel(channel_id)
            await text_channel.send(self.msg.value)
            return await interaction.response.send_message(f"Message sent in {text_channel.mention}",ephemeral=True)
        except Exception as e:          
            return await interaction.response.send_message(f"Error : {e}",ephemeral=True)
            


    