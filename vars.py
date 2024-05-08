import os

from dotenv import load_dotenv
from pyromod.helpers import ikb
from pyromod.helpers import helpers as pyromod_helpers

load_dotenv()


class Vars(object):

    API_ID: int = int(os.environ.get('API_ID'))
    API_HASH: str = os.environ.get('API_HASH')
    BOT_TOKEN: str = os.environ.get('BOT_TOKEN')

    TIMEOUT: int = 60

    JOB_POST: str = """
Job Title: {}
Seniority: {}
Job Link: {}
""".strip()

    ADMIN_ID = 1752221538
    CHANNEL_ID = -1002091947120


class Buttons(object):

    DEV_TYPE_BUTTONS: pyromod_helpers = ikb(
        [
            [("Java Developer", "java_dev")],
            [("iOS Developer", "ios_dev")],
            [("Flutter Developer", "flutter_dev")],
            [("Android Developer", "android_dev")],
            [("QA Engineer", "qa_engineer")],
        ]
    )

    SENIORITY_BUTTONS: pyromod_helpers = ikb(
        [
            [("Intern", "intern")],
            [("Junior", "junior")],
            [("Middle", "middle")],
            [("Senior", "senior")],
            [("Lead", "lead")],
            [("Architect", "architect")],
        ]
    )

    SUBMIT_BUTTONS: pyromod_helpers = ikb(
        [
            [("Submit ✅", "submit")],
            [("Cancel ❌", "cancel")],
        ]
    )

    APPROVING_BUTTONS: pyromod_helpers = ikb(
        [
            [("Varify ✅", "verify")],
            [("delete ❌", "delete")],
        ]
    )


class Tags(object):

    LIST: dict[str: str] = {
        "java_dev": '#java',
        "ios_dev": '#ios',
        "flutter_dev": '#flutter',
        "android_dev": '#android',
        "qa_engineer": '#qa',
    }
