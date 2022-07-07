# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from time import time
from json import loads
from os import path, remove, stat
from typing import Callable, Union
from asyncio import sleep, wait_for, get_event_loop

from config import Config
from aiofiles import open
from pyrogram import Client
from gofile2 import Async_Gofile
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery
from pyromod import listen

from .database.users import check_user
from .helpers_nexa.buttons import Buttons
from .database.upload_mode import get_upload_mode
from .helpers_nexa.utils import (TimeFormatter, get_or_gen_thumb,
                                 progress_for_pyrogram, rm_mark_chars,
                                 run_shell_cmds)


class UnzipBot(Client):

    # Bot version
    nx_version = "v1.0"

    def __init__(self, name: str, api_id: Union[int, str], api_hash: str, bot_token: str, plugins: dict, sleep_threshold: int):
        super().__init__(name, api_id, api_hash, bot_token, plugins, sleep_threshold)

    def handler_func(self) -> Callable:
        """
        Handle erros and database updates of users
        """
        def decorator(func: Callable) -> Callable:
            async def wrapper(client: Client, message: Message):
                try:
                    await check_user(message)
                    await func(client, message)
                except Exception as e:
                    await self.send_message(message.chat.id, (await self.get_string("failed_main")).format(e))

            return wrapper

        return decorator

    async def ask_user(self, c_id: int, text: str, timeout: float = None, *args, **kwargs):
        """
        Get an input from a user

        Parameters:

            - `c_id` - Chat id
            - `text` - Message text
            - `timeout` - Timeout in seconds
        """
        async def listen_to(timeout: float):
            future = get_event_loop().create_future()
            return await wait_for(future, timeout)

        await self.send_message(c_id, text, *args, **kwargs)
        resp = await listen_to(timeout)
        return resp

    async def send_file(self, c_id: int, doc_f: str, query: CallbackQuery):
        """
        Send a file to the user

        Parameters:

            - `c_id` - Chat id
            - `doc_f` - File path
            - `query` - CallBackQuery object
        """
        try:
            cum = await get_upload_mode(c_id)
            # Checks if url file size is bigger than 2GB (Telegram limit)
            file_size = stat(doc_f).st_size
            if file_size > Config.TG_MAX_SIZE:
                # Uploads the file to gofile.io
                upmsg = await self.send_message(c_id, text=await self.get_string("alert_file_too_large"))
                try:
                    ga = Async_Gofile()
                    gfio = await ga.upload(doc_f)
                    await upmsg.edit("**Your file has been uploaded to gofile! Click on the below button to download it 👇**", reply_markup=await Buttons.make_button("Gofile link 🔗", url=gfio["downloadPage"]))
                except:
                    await upmsg.edit("`Upload failed, Better luck next time 😔!`")
                remove(doc_f)
                return

            tgupmsg = await self.send_message(c_id, await self.get_string("processing"))
            stm = time()

            # Uplaod type: Video
            if cum == "video":
                sthumb = await get_or_gen_thumb(c_id, doc_f, True)
                vid_duration = await run_shell_cmds(f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {doc_f}")
                await self.send_video(
                    chat_id=c_id,
                    video=doc_f,
                    caption="**Extracted by @NexaUnzipper_Bot**",
                    duration=int(
                        vid_duration) if vid_duration.isnumeric() else 0,
                    thumb=sthumb,
                    progress=progress_for_pyrogram,
                    progress_args=("**Trying to upload 😇** \n", tgupmsg, stm))
            # Upload type: Document
            else:
                sthumb = await get_or_gen_thumb(c_id, doc_f)
                await self.send_document(
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
        
**File name:** `{path.basename(doc_f)}`
**Uploaded in:** `{TimeFormatter(round(etm - stm))}`


**Join @NexaBotsUpdates ❤️**
        """)
            # Cleanup (Added try except as thumbnail is sucking this code's duck)
            try:
                remove(doc_f)
                if sthumb:
                    remove(sthumb)
            except:
                pass
        except FloodWait as f:
            await sleep(f.x)
            return await self.send_file(c_id, doc_f, query)
        except FileNotFoundError:
            try:
                return await query.answer("Sorry! I can't find that file", show_alert=True)
            except:
                return await self.send_message(c_id, "Sorry! I can't find that file")
        except BaseException as e:
            print(e)
            await self.answer_query(query, f"**Error:** \n`{e}`")

    async def answer_query(self, query: CallbackQuery, text: str, alert: bool = False, *args, **kwargs):
        """
        Answer CallbackQuery with better error handling

        Parameters:

            - `query` - CallBackQuery object
            - `text` - Message text
            - `alert` - Pass True if you want to show the message as an alert
        """
        try:
            if alert:
                await query.answer(await rm_mark_chars(text), show_alert=True, *args, **kwargs)
            else:
                await query.message.edit(text, *args, **kwargs)
        except:
            try:
                query.message.delete()
            except:
                pass
            await self.send_message(query.message.chat.id, text, *args, **kwargs)

    async def get_string(self, key: str) -> str:
        """
        Get the text string according to the saved language type

        Parameters:

            - `key` - String key
        """
        lang = "en"
        async with open(f"unzipper/data/{lang}/messages.json") as ls:
            jsn = loads(await ls.read())
            return jsn.get(key)


unzipperbot = UnzipBot(
    "UnzipperBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=dict(root="unzipper/modules"),
    sleep_threshold=10
)
