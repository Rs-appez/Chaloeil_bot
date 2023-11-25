from decouple import config

#debug
DEBUG=config('DEBUG',default=False)

#token
CHALOEIL_TOKEN=config('CHALOEIL_TOKEN')
BACKEND_TOKEN=config('BACKEND_TOKEN')

#guild
CELLAR_GUILD_ID=config("CELLAR_GUILD_ID")
DELIRE_GUILD_ID=config("DELIRE_GUILD_ID")

#channel
CHANNELBOT_LOG_ID=1110930833314938950

#user
CHALOEIL_ID=config("CHALOEIL_ID")

#url
BACKEND_URL=config("BACKEND_URL")