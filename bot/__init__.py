from pyrogram.enums import ParseMode

from consts import Consts
from pyromod import Client

app: Client = Client(
    "bot",
    api_id=Consts.API_ID,
    api_hash=Consts.API_HASH,
    bot_token=Consts.BOT_TOKEN,
    parse_mode=ParseMode.MARKDOWN
)

import bot.callbacks
