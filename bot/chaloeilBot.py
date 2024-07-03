from nextcord import CustomActivity, ChannelType, Message
import nextcord
from nextcord.ext import commands
import config
import bleach

class ChaloeilBot(commands.Bot):

    def __init__(self, command_prefix):

        self.voice_client = None
        intents = nextcord.Intents.default()
        intents.members = True
        intents.voice_states = True
        intents.message_content = True
        super().__init__(command_prefix, intents=intents,activity=CustomActivity(name="Custom Status",state="I want to play a game"))

        self.ch_emojis = {}

    async def on_ready(self):
        print(f"{self.user.display_name} est pret")
        if not config.DEBUG:
            cellar = self.get_guild(int(config.CELLAR_GUILD_ID))
            if cellar :
                self.ch_emojis["chaloeil"] = await cellar.fetch_emoji(1119363924907790406)
                msg = await cellar.get_channel(int(config.CHANNELBOT_LOG_ID)).send("UP !")
                await msg.add_reaction(self.ch_emojis["chaloeil"])
            await self.get_emojis()

    async def get_emojis(self):

        guild = self.get_guild(int(config.DELIRE_GUILD_ID))
        if guild :
            self.ch_emojis["delire"] = await guild.fetch_emoji(1027165356168593478)

    async def on_message(self,message : Message):
        print("ok")
        if message.author == self.user:
            return

        message.content = bleach.clean(message.content)

        if message.content.startswith(self.command_prefix):
            await self.process_commands(message)

        elif message.channel.type == ChannelType.private:

            guild = self.get_guild(int(config.CHALOEIL_GUILD_ID))
            if guild :
                files = []
                for file in message.attachments:
                    files.append(await file.to_file())
                await guild.get_channel(int(config.CHANEL_DM_ID)).send(content=f"**__{message.author} dm me __*: \n{message.content}",embeds=message.embeds,files=files)


