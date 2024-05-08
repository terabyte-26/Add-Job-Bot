from vars import Vars
from pyromod import Client

app: Client = Client("bot", api_id=Vars.API_ID, api_hash=Vars.API_HASH, bot_token=Vars.BOT_TOKEN)

import bot.callbacks
