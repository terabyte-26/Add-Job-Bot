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
Job Link: {}
""".strip()


class Buttons(object):

    DEV_TYPE_BUTTONS: pyromod_helpers = ikb(
        [
            [("Java Developer", "java_dev")],
            [("iOS Developer", "ios_dev")],
            [("Flutter Developer", "flutter_dev")],
            [("iOS Developer", "ios_dev")],
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

    SUBMIT_BUTTONS: pyromod_helpers = ikb(
        [
            [("Submit ✅", "submit")],
            [("Cancel ❌", "cancel")],
        ]
    )


class Lists(object):

    DEVELOPERS_TYPES: list[str] = [
        "java_dev",
        "ios_dev",
        "flutter_dev",
        "ios_dev",
        "android_dev",
        "qa_engineer",
    ]

    SENIORITY_LEVELS: list[str] = [
        'intern',
        'junior',
        'middle',
        'senior',
        'lead',
        'architect',
    ]
