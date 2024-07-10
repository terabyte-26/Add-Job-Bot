from consts import Consts
from pyromod import Client

app: Client = Client("bot", api_id=Consts.API_ID, api_hash=Consts.API_HASH, bot_token=Consts.BOT_TOKEN)

import bot.callbacks
