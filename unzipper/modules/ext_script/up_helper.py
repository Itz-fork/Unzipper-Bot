# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

import os
import re
import shutil
import asyncio

from pyrogram.errors import FloodWait
from config import Config

# Send file to a user
async def send_file(unzip_bot, c_id, doc_f, query, full_path):
    try:
        # Checks if url file size is bigger than 2GB (Telegram limit)
        u_file_size = os.stat(doc_f).st_size
        if Config.TG_MAX_SIZE < int(u_file_size):
            return await unzip_bot.send_message(
                chat_id=c_id,
                text="`File Size is too large to send in telegram 🥶!` \n\n**Sorry, but I can't do anything about this as it's a telegram limitation 😔!**"
            )
        await unzip_bot.send_document(chat_id=c_id, document=doc_f, caption="**Extracted by @NexaUnzipper_Bot**")
        os.remove(doc_f)
    except FloodWait as f:
        asyncio.sleep(f.x)
        return send_file(c_id, doc_f)
    except FileNotFoundError:
        await query.answer("Sorry! I can't find that file", show_alert=True)
    except BaseException:
        shutil.rmtree(full_path)


# Function to remove basic markdown characters from a string
async def rm_mark_chars(text: str):
    return re.sub("[*`_]", "", text)


# Function to answer queries
async def answer_query(query, message_text: str, answer_only: bool = False, unzip_client = None):
    try:
        if answer_only:
            await query.answer(await rm_mark_chars(message_text), show_alert=True)
        else:
            await query.message.edit(message_text)
    except:
        if unzip_client:
            await unzip_client.send_message(chat_id=query.message.chat.id, text=message_text)