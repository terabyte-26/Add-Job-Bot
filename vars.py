import os
from uuid import UUID

from dotenv import load_dotenv

load_dotenv()

class Vars(object):

    API_ID: int = int(os.environ.get('API_ID'))
    API_HASH: str = os.environ.get('API_HASH')
    BOT_TOKEN: str = os.environ.get('BOT_TOKEN')


class TempVars(Vars):
    Temporary_Vars: dict[str, dict] = {}
