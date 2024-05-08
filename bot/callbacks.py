from bot import app
from vars import Vars, Buttons, Tags

from pyromod import Client
from pyromod.types import ListenerTypes

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pyrogram import enums


@app.on_message(filters.command(['start']) & filters.private)
async def start_command(c: Client, m: Message):
    is_member_in_group: bool = False
    chat_id: int = m.chat.id

    f_name = m.chat.first_name
    l_name = m.chat.last_name

    # Is member or not
    try:
        await c.get_chat_member(Vars.GROUP_ID, chat_id)
        is_member_in_group = True
    except:
        pass

    user_name: str = f'{f_name} {l_name}'

    if is_member_in_group:
        await c.send_message(
            chat_id=chat_id,
            text=f"Welcome Back {user_name}, You can Use /add_job command, and follow the Steps to Add a new Job Post"
        )

    else:
        await c.send_message(
            chat_id=chat_id,
            text=f"Hello {user_name},\nPlease Join our Group To be Able to Start Posting Jobs, Then retuen and Click on 'Joined' Button To Start The Bot",
            reply_markup=Buttons.JOIN_GROUP_BUTTONS
        )


@app.on_message(filters.command(['add_job']) & filters.private)
async def add_job(c: Client, m):
    chat_id: int = m.chat.id

    try:
        await c.get_chat_member(Vars.GROUP_ID, chat_id)
    except:
        await start_command(c, m)
        return

    await app.send_chat_action(chat_id, enums.ChatAction.TYPING)

    developers_type_response = await c.ask(
        chat_id=chat_id,
        text="You are a:",
        timeout=Vars.TIMEOUT,
        listener_type=ListenerTypes.CALLBACK_QUERY,
        reply_markup=Buttons.DEV_TYPE_BUTTONS
    )

    developers_type = developers_type_response.data

    list_of_buttons: list[[InlineKeyboardMarkup]] = developers_type_response.message.reply_markup.inline_keyboard
    text_developer = [button[0].text for button in list_of_buttons if button[0].callback_data == developers_type][0]

    '''# region Title Handler
    title_response: Client = await c.ask(
        chat_id=chat_id,
        text=f"What is the job's title as a {text_developer}?\n",
        timeout=timeout,
        filters=filters.text
    )

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

    title_text = title_response.text
    # endregion'''

    seniority_levels_response = await c.ask(
        chat_id=chat_id,
        text="Seniority :",
        timeout=Vars.TIMEOUT,
        listener_type=ListenerTypes.CALLBACK_QUERY,
        reply_markup=Buttons.SENIORITY_BUTTONS
    )

    seniority_level = seniority_levels_response.data

    list_of_buttons: list[[InlineKeyboardMarkup]] = seniority_levels_response.message.reply_markup.inline_keyboard
    text_seniority_level = [button[0].text for button in list_of_buttons if button[0].callback_data == seniority_level][
        0]

    description_response: Client = await c.ask(
        chat_id=chat_id,
        text=f"So you are a {text_seniority_level} {text_developer},\n Please Send the Description Image",
        timeout=Vars.TIMEOUT,
        filters=filters.photo
    )

    description_photo = description_response.photo.file_id

    job_link_response = await c.ask(
        chat_id=chat_id,
        text=f"Kindly, Provide the link of this job",
        timeout=Vars.TIMEOUT,
        filters=filters.text
    )

    job_link = job_link_response.text

    await c.send_photo(
        chat_id=chat_id,
        photo=description_photo,
    )

    submit_response = await c.ask(
        chat_id=chat_id,
        text=Vars.JOB_POST.format(
            text_developer,
            text_seniority_level,
            job_link
        ),
        timeout=Vars.TIMEOUT,
        listener_type=ListenerTypes.CALLBACK_QUERY,
        reply_markup=Buttons.SUBMIT_BUTTONS
    )

    print(submit_response)

    submit: bool = True if submit_response.data == "submit" else False

    if submit:

        caption = Vars.JOB_POST.format(
            text_developer,
            text_seniority_level,
            job_link
        ) + '\n\n' + Tags.LIST[developers_type]

        await c.send_photo(
            chat_id=Vars.ADMIN_ID,
            photo=description_photo,
            caption=caption,
            reply_markup=Buttons.APPROVING_BUTTONS
        )

    else:

        current_message_id: int = submit_response.message.id

        await c.delete_messages(
            chat_id=chat_id,
            message_ids=[
                current_message_id,
                current_message_id-1,
            ]
        )


@app.on_callback_query()
async def callback(c: Client, q):
    chat_id: int = q.from_user.id

    data = q.data
    m: Message = q.message

    if data in 'verify':
        photo = m.photo.file_id
        caption = m.caption
        caption_entities = m.caption_entities

        await c.send_photo(
            chat_id=Vars.GROUP_ID,
            photo=photo,
            caption=caption,
            caption_entities=caption_entities
        )

    if data in 'delete':
        await q.message.delete()

    if data in 'joined':
        await start_command(c, m)


@app.on_message(filters.group & filters.text)
async def tst(_, __):
    pass
