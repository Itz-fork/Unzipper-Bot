# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

import os
import re
import shutil
import subprocess

from time import time
from asyncio import sleep
from config import Config
from gofile2 import Async_Gofile
from unzipper import unzipperbot
from pyrogram.errors import FloodWait
from unzipper.modules.bot_data import Buttons
from unzipper.helpers_nexa.database.thumbnail import get_thumbnail
from unzipper.helpers_nexa.database.upload_mode import get_upload_mode
from unzipper.helpers_nexa.unzip_help import progress_for_pyrogram, TimeFormatter


# To get video duration and thumbnail
async def run_shell_cmds(command):
    run = subprocess.Popen(command, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, shell=True)
    shell_ouput = run.stdout.read()[:-1].decode("utf-8")
    return shell_ouput


# Returns thumbnail path
async def get_or_gen_thumb(uid, doc_f, isvid=False):
    dbthumb = await get_thumbnail(int(uid))
    if dbthumb:
        return dbthumb
    elif isvid:
        thmb_pth = f"Dump/thumbnail_{os.path.basename(doc_f)}.jpg"
        if os.path.exists(thmb_pth):
            os.remove(thmb_pth)
        await run_shell_cmds(f"ffmpeg -ss 00:00:01.00 -i {doc_f} -vf 'scale=320:320:force_original_aspect_ratio=decrease' -vframes 1 {thmb_pth}")
        return thmb_pth
    else:
        return None


# Send file to a user
async def send_file(c_id, doc_f, query, full_path):
    try:
        cum = await get_upload_mode(c_id)

        # Checks if url file size is bigger than 2GB (Telegram limit)
        u_file_size = os.stat(doc_f).st_size
        if Config.TG_MAX_SIZE < int(u_file_size):
            # Uploads the file to gofile.io
            upmsg = await unzipperbot.send_message(
                chat_id=c_id,
                text="`File Size is too large to send in telegram 🥶! Trying to upload this file to gofile.io now 😉!`"
            )
            try:
                ga = Async_Gofile()
                gfio = await ga.upload(doc_f)
                await upmsg.edit("**Your file has been uploaded to gofile! Click on the below button to download it 👇**", reply_markup=Buttons().GOFILE_BTN(gfio["downloadPage"]))
            except:
                await upmsg.edit("`Upload failed, Better luck next time 😔!`")
            os.remove(doc_f)
            return

        tgupmsg = await unzipperbot.send_message(c_id, "`Processing ⚙️...`")
        stm = time()
        # Uplaod type: Video
        if cum == "video":
            sthumb = await get_or_gen_thumb(c_id, doc_f, True)
            vid_duration = await run_shell_cmds(f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {doc_f}")
            await unzipperbot.send_video(
                chat_id=c_id,
                video=doc_f,
                caption="**Extracted by @NexaUnzipper_Bot**",
                duration=int(vid_duration) if vid_duration.isnumeric() else 0,
                thumb=sthumb,
                progress=progress_for_pyrogram,
                progress_args=("**Trying to upload 😇** \n", tgupmsg, stm))
        # Upload type: Document
        else:
            sthumb = await get_or_gen_thumb(c_id, doc_f)
            await unzipperbot.send_document(
                chat_id=c_id,
                document=doc_f,
                caption="**Extracted by @NexaUnzipper_Bot**",
                thumb=sthumb,
                progress=progress_for_pyrogram,
                progress_args=("**Trying to upload 😇** \n", tgupmsg, stm))
        etm = time()
        # Edit the progress message
        await tgupmsg.edit(f"""
**Successfully uploaded!**
        
**File name:** `{os.path.basename(doc_f)}`
**Uploaded in:** `{TimeFormatter(round(etm - stm))}`


**Join @NexaBotsUpdates ❤️**
        """)
        # Cleanup (Added try except as thumbnail is sucking this code's duck)
        try:
            os.remove(doc_f)
            if sthumb:
                os.remove(sthumb)
        except:
            pass
    except FloodWait as f:
        sleep(f.x)
        return await send_file(c_id, doc_f, query, full_path)
    except FileNotFoundError:
        try:
            return await query.answer("Sorry! I can't find that file", show_alert=True)
        except:
            return await unzipperbot.send_message(c_id, "Sorry! I can't find that file")
    except BaseException as e:
        print(e)
        shutil.rmtree(full_path)


# Function to remove basic markdown characters from a string
async def rm_mark_chars(text: str):
    return re.sub("[*`_]", "", text)


# Function to answer queries
async def answer_query(query, message_text: str, answer_only: bool = False, unzip_client=None):
    try:
        if answer_only:
            await query.answer(await rm_mark_chars(message_text), show_alert=True)
        else:
            await query.message.edit(message_text)
    except:
        if unzip_client:
            await unzip_client.send_message(chat_id=query.message.chat.id, text=message_text)
