import asyncio

from bot import app
from consts import Consts, Buttons, Tags

from pyromod import Client
from pyromod.types import ListenerTypes

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram import enums


# start Command Handler
@app.on_message(filters.command(['start']) & filters.private)
async def start_command(c: Client, m: Message):
    is_member_in_group: bool = False
    chat_id: int = m.chat.id

    f_name: str = m.chat.first_name
    l_name: str = m.chat.last_name

    # Is member or not
    try:
        await c.get_chat_member(Consts.PUBLIC_CHANNEL, chat_id)
        is_member_in_group: bool = True
    except:
        pass

    user_name: str = f'{f_name} {l_name}'

    # If the user member on the group
    if is_member_in_group:
        await c.send_message(
            chat_id=chat_id,
            text=f"Welcome Back {user_name}, You can Use **Add job**, and **follow the Steps to --Add a new Job Post--**",
            reply_markup=Buttons.ADD_JOB_BUTTONS
        )

    # If the user not a member
    else:
        await c.send_message(
            chat_id=chat_id,
            text=f"Hello {user_name},\nPlease --Subscribe-- on our **[Channel]({Consts.CHANNEL_LINK})** To be Able to Start Posting Jobs, Then retuen and Click on 'Subscribed' Button To Start The Bot",
            reply_markup=Buttons.JOIN_GROUP_BUTTONS
        )


# add_job Command Handler
@app.on_message(filters.command(['add_job']) & filters.private)
async def add_job(c: Client, m: Message):


    chat_id: int = m.chat.id

    # Check if the user is member on the Group
    try:
        await c.get_chat_member(Consts.PUBLIC_CHANNEL, chat_id)
    except:
        await start_command(c, m)
        return

    # Send Typing Action
    await app.send_chat_action(chat_id, enums.ChatAction.TYPING)

    developers_type_response = await c.ask(
        chat_id=chat_id,
        text="You are a:",
        timeout=Consts.TIMEOUT,
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
        timeout=Consts.TIMEOUT,
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
        timeout=Consts.TIMEOUT,
        filters=filters.photo
    )

    description_photo = description_response.photo.file_id

    job_link_response = await c.ask(
        chat_id=chat_id,
        text=f"Kindly, Provide the link of this job",
        timeout=Consts.TIMEOUT,
        filters=filters.text
    )

    job_link = job_link_response.text

    await c.send_photo(
        chat_id=chat_id,
        photo=description_photo,
    )

    submit_response = await c.ask(
        chat_id=chat_id,
        text=Consts.JOB_POST.format(
            text_developer,
            text_seniority_level,
            job_link
        ),
        timeout=Consts.TIMEOUT,
        listener_type=ListenerTypes.CALLBACK_QUERY,
        reply_markup=Buttons.SUBMIT_BUTTONS
    )

    submit: bool = True if submit_response.data == "submit" else False
    current_message_id: int = submit_response.message.id

    if submit:

        caption = Consts.JOB_POST.format(
            text_developer,
            text_seniority_level,
            job_link
        ) + '\n\n' + Tags.LIST[developers_type]



        await c.send_photo(
            chat_id=Consts.ADMINS_GROUP_ID,
            photo=description_photo,
            caption=caption,
            reply_markup=Buttons.APPROVING_BUTTONS
        )

    await c.delete_messages(
        chat_id=chat_id,
        message_ids=[
            current_message_id,
            current_message_id - 1,
        ]
    )

    if submit:
        await c.send_message(
            chat_id=chat_id,
            text='✅',
        )






@app.on_callback_query()
async def callback(c: Client, q: CallbackQuery):
    chat_id: int = q.from_user.id

    print('chat_id', chat_id)

    data = q.data
    m: Message = q.message

    print('data', data)

    if chat_id in Consts.ADMIN_IDS:

        print('ok')

        if data in 'verify':
            print('verify')

            photo = m.photo.file_id
            caption = m.caption
            caption_entities = m.caption_entities

            await c.send_photo(
                chat_id=Consts.PUBLIC_CHANNEL,
                photo=photo,
                caption=caption,
                caption_entities=caption_entities
            )

            await q.message.delete()

            validation_icon_message: Message = await c.send_message(
                chat_id=Consts.ADMINS_GROUP_ID,
                text='✅',
            )

            await asyncio.sleep(2)
            await validation_icon_message.delete()

        if data in 'reject':
            await q.message.delete()

    if data in 'subscribed':
        await start_command(c, m)

    if data in 'add_job':
        await add_job(c, q.message)


@app.on_message(filters.group & filters.text)
async def tst(_, m: Message):
    print(m)
    pass
