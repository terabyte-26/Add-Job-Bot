from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup
from pyromod.types import ListenerTypes

from bot import app
from vars import Vars, Buttons, Tags
from pyromod import Client
from pyromod.helpers import ikb
from pyrogram import enums


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
async def add_job(c: Client, m):
    red_flag = False
    rewarded_id = None
    chat_id = m.chat.id

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

    submit = True if submit_response.data == "submit" else False



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
    chat_id = q.from_user.id

    data = q.data
    m = q.message

    if data in 'verify':


        photo = m.photo.file_id
        caption = m.caption
        caption_entities = m.caption_entities

        await c.send_photo(
            chat_id=Vars.CHANNEL_ID,
            photo=photo,
            caption=caption,
            caption_entities=caption_entities
        )


    if data in 'delete':
        pass

        await q.message.delete()

    pass


@app.on_message(filters.group & filters.text)
async def tst(c: Client, m):
    print(m)


'''    if q_data in Lists.DEVELOPERS_TYPES:
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


        print(TempVars.Temporary_Vars)'''
