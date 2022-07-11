# ===================================================================== #
#                      Copyright (c) 2022 Itz-fork                      #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  #
# See the GNU General Public License for more details.                  #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>   #
# ===================================================================== #

import logging
from time import time
from json import loads
from asyncio import sleep
from typing import Callable
from os import path, remove, stat

from aiofiles import open
from config import Config
from pyrogram import Client
from gofile2 import Async_Gofile
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, Message

from .database.users import check_user
from .helpers_nexa.buttons import Buttons
from .database.thumbnail import get_or_gen_thumb
from .database.upload_mode import get_upload_mode
from .helpers_nexa.utils import (TimeFormatter, progress_for_pyrogram,
                                 rm_mark_chars, run_shell_cmds)



class CustomMethods:
    version = "v1.0 - Beta"

    def __init__(self) -> None:
        super().__init__()
    
    def handle_erros(self: Client, func: Callable) -> Callable:
        """
        Handle erros and database updates of users
        """

        async def decorator(client: Client, message: Message):
            try:
                await check_user(message)
                return await func(client, message)
            except Exception as e:
                logging.warn(e)
                await self.send_message(message.chat.id, (await self.get_string("failed_main")).format(e))

        return decorator
    
    def handle_callbacks(self: Client, func: Callable) -> Callable:
        """
        Handle erros and database updates of users
        """

        async def decorator(client: Client, query: CallbackQuery):
            try:
                await func(client, query)
            except Exception as e:
                logging.warn(e)
                await self.send_message(query.message.chat.id, (await self.get_string("failed_main")).format(e))

        return decorator

    async def send_file(self: Client, c_id: int, doc_f: str, query: CallbackQuery):
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
            logging.warn(e)
            await self.answer_query(query, f"**Error:** \n`{e}`")

    async def answer_query(self: Client, query: CallbackQuery, text: str, alert: bool = False, *args, **kwargs):
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

    async def get_string(self: Client, key: str) -> str:
        """
        Get the text string according to the saved language type

        Parameters:

            - `key` - String key
        """
        lang = "en"
        async with open(f"unzipper/data/{lang}/messages.json") as ls:
            jsn = loads(await ls.read())
            return jsn.get(key)


def apply_patch():
    """
    Apply custom methods defined in CustomMethods class to pyrogram.Client class
    """
    for ckey, cval in CustomMethods.__dict__.items():
        if ckey[:2] != "__":
            setattr(Client, ckey, cval)