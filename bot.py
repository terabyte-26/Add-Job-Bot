import uuid



from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyromod.exceptions import ListenerTimeout
from pyromod.types import ListenerTypes

from vars import Vars, TempVars

from pyromod import Client, Message
from pyromod.helpers import ikb
from pyrogram import enums

app: Client = Client("bot", api_id=Vars.API_ID, api_hash=Vars.API_HASH, bot_token=Vars.BOT_TOKEN)


developers_types = [
    "java_dev",
    "ios_dev",
    "flutter_dev",
    "ios_dev",
    "android_dev",
    "qa_engineer",
]

seniority_levels = [
    'intern',
    'junior',
    'middle',
    'senior',
    'lead',
    'architect',
]


timeout = 60



'''@app.on_message(filters.command(['start']) & filters.private)
async def start_command(c: Client, m):
    red_flag = False
    rewarded_id = None
    chat_id = m.chat.id

    # await app.send_message(chat_id,'Hello')

    resp = await app.ask(chat_id=chat_id, text="**Welcome to Jobs Bot!**", reply_markup=dev_type, timeout=60)

    print(resp)

    print(m)'''


@app.on_message(filters.command(['add_job']) & filters.private)
async def start_command(c: Client, m):
    red_flag = False
    rewarded_id = None
    chat_id = m.chat.id

    temp_id = str(uuid.uuid4())[:8]
    print(temp_id)

    dev_type = ikb(
        [
            [("Java Developer",  f"{temp_id}|java_dev")],
            [("iOS Developer",  f"{temp_id}|ios_dev")],
            [("Flutter Developer",  f"{temp_id}|flutter_dev")],
            [("iOS Developer",  f"{temp_id}|ios_dev")],
            [("Android Developer",  f"{temp_id}|android_dev")],
            [("QA Engineer",  f"{temp_id}|qa_engineer")],
        ]
    )

    TempVars.Temporary_Vars[chat_id] = {
        temp_id: {}
    }

    await app.send_chat_action(chat_id, enums.ChatAction.TYPING)
    await app.send_message(chat_id=chat_id, text="You are a:", reply_markup=dev_type)


@app.on_callback_query()
async def callback(c: Client, q):
    chat_id = q.from_user.id
    temp_id: str = q.data.split("|")[0]
    q_data = q.data.split("|")[1]


    if q_data in developers_types:
        list_of_buttons: list[[InlineKeyboardMarkup]] = q.message.reply_markup.inline_keyboard
        text_developer = [button[0].text for button in list_of_buttons if button[0].callback_data.split("|")[1] == q_data][0]

        try:


            # region Title Handler
            title_response: Client = await c.ask(chat_id=chat_id, text=f"`{temp_id}`\nWhat is the job's title as a {text_developer}?\n", timeout=timeout, filters=filters.text)
            counter = 0
            while not title_response.text.lower().startswith('title: '):

                title_response: Client = await c.ask(chat_id=chat_id,
                                                     text=f"Please put the title as the format:\ntitle: 'title here'",
                                                     timeout=timeout, filters=filters.text
                                                     )

                if counter > 2:
                    await c.send_message(chat_id=chat_id,
                                text=f"You can Cancel the process by sendind 'cancel'",
                                timeout=timeout, filters=filters.text
                                )
                counter += 1


            # endregion

            TempVars.Temporary_Vars[chat_id][temp_id]['job_title'] = title_response.text

            seniority = ikb(
                [
                    [("Intern", f"{temp_id}|intern")],
                    [("Junior", f"{temp_id}|junior")],
                ]
            )

            seniority_response: Client = await c.ask(
                chat_id=chat_id,
                text=f"Seniority :",
                timeout=timeout,
                listener_type=ListenerTypes.CALLBACK_QUERY,
                reply_markup=seniority
            )

            print(seniority_response)
            print('good')

        except ListenerTimeout:
            await q.message.reply('You took too long to answer.')

            if temp_id:
                del TempVars.Temporary_Vars[temp_id]

    if q_data in seniority_levels:

        TempVars.Temporary_Vars[chat_id][temp_id]['seniority_level'] = q_data

        # region Description Handler
        description_response: Client = await c.ask(chat_id=chat_id, text=f"Please Send the Description Image",
                                                   timeout=timeout, filters=filters.photo)
        print(description_response)

        is_image = False
        try:
            if description_response.photo.file_id:
                is_image = True
        except:
            is_image = False

        # await c.send_photo(chat_id=chat_id, photo=description_response.photo.file_id)

        while is_image is False:
            description_response: Client = await c.ask(chat_id=chat_id,
                                                       text=f"What is the Description Text",
                                                       timeout=timeout, filters=filters.text
                                                       )

            try:
                if description_response.photo.file_id:
                    is_image = True
            except:
                is_image = False
        # endregion


        print(TempVars.Temporary_Vars)
