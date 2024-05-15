import os
from bot.chaloeilBot import ChaloeilBot
import config

from interaction_discord_bot.init_cog import init_cog

debug = config.DEBUG

if debug :
    cmd_prefix = "§"
else :
    cmd_prefix = "!"


chaloeil = ChaloeilBot(cmd_prefix)

for file in os.listdir("./cogs"):
    if(file.endswith(".py")):
        chaloeil.load_extension(f"cogs.{file[:-3]}")

init_cog(chaloeil)

chaloeil.run(config.CHALOEIL_TOKEN) 