import os
from bot.chaloeilBot import ChaloeilBot
import config

debug = config.DEBUG

if debug :
    cmd_prefix = "§"
else :
    cmd_prefix = "!"


chaloeil = ChaloeilBot(cmd_prefix)

for file in os.listdir("./cogs"):
    if(file.endswith(".py")):
        chaloeil.load_extension(f"cogs.{file[:-3]}")

chaloeil.run(config.CHALOEIL_TOKEN)