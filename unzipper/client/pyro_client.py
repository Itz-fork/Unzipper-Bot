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
from asyncio import sleep
from typing import Callable
from os import path, remove, stat

from config import Config
from pyrogram import Client
from .caching import STRINGS
from gofile2 import Async_Gofile
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, Message
from unzipper.database.language import get_language
from unzipper.database.upload_mode import get_upload_mode
from unzipper.helpers_nexa.utils import (TimeFormatter, progress_for_pyrogram,
                                         rm_mark_chars, run_shell_cmds)


class UnzipperBot(Client):
    """
    Unzipper bot client
    """
    version = "v1.0.2"

    def __init__(self):
        super().__init__("UnzipperBot",
                         api_id=Config.APP_ID,
                         api_hash=Config.API_HASH,
                         bot_token=Config.BOT_TOKEN,
                         plugins=dict(root="unzipper/modules"),
                         sleep_threshold=10)

    ######## Decorators ########
    def handle_erros(self, func: Callable) -> Callable:
        """
        Handle erros and database updates of users
        """

        async def decorator(client: Client, message: Message):
            lang = await get_language(message.chat.id)
            try:
                await self.check_user(message)
                return await func(client, message, STRINGS[lang])
            except Exception as e:
                logging.warn(e)
                await self.send_message(message.chat.id, STRINGS[lang]["failed_main"].format(e))

        return decorator

    def handle_query(self, func: Callable) -> Callable:
        """
        Handle callback queries
        """

        async def decorator(client: Client, query: CallbackQuery):
            lang = await get_language(query.message.chat.id)
            try:
                await func(client, query, STRINGS[lang])
            except Exception as e:
                logging.warn(e)
                await self.send_message(query.message.chat.id, STRINGS[lang]["failed_main"].format(e))

        return decorator

    ######## File utils ########
    async def send_file(self, c_id: int, doc_f: str, query: CallbackQuery, lang: str = "en", del_status: bool = False):
        """
        Send a file to the user

        Parameters:

            - `c_id` - Chat id
            - `doc_f` - File path
            - `query` - CallBackQuery object
            - `del_status` - Whether if you want to delete progress message or not
        """

        try:
            # This is my kingdom...
            cum = await get_upload_mode(c_id)
            # Checks if url file size is bigger than 2GB (Telegram limit)
            file_size = stat(doc_f).st_size
            if file_size > Config.TG_MAX_SIZE:
                # Uploads the file to gofile.io
                upmsg = await self.send_message(c_id, text=STRINGS[lang]["alert_file_too_large"])
                try:
                    ga = Async_Gofile()
                    gfio = await ga.upload(doc_f)
                    from unzipper import Buttons
                    await upmsg.edit("**Your file has been uploaded to gofile! Click on the below button to download it 👇**", reply_markup=await Buttons.make_button("Gofile link 🔗", url=gfio["downloadPage"]))
                except:
                    await upmsg.edit("`Upload failed, Better luck next time 😔!`")
                remove(doc_f)
                return

            tgupmsg = await self.send_message(c_id, STRINGS[lang]["processing"])
            stm = time()

            # Uplaod type: Video
            if cum == "video":
                sthumb = await self.get_or_gen_thumb(c_id, doc_f, True)
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
                sthumb = await self.get_or_gen_thumb(c_id, doc_f)
                await self.send_document(
                    chat_id=c_id,
                    document=doc_f,
                    caption="**Extracted by @NexaUnzipper_Bot**",
                    thumb=sthumb,
                    progress=progress_for_pyrogram,
                    progress_args=("**Trying to upload 😇** \n", tgupmsg, stm))
            etm = time()

            # Delete or edit the progress message
            await tgupmsg.delete() if del_status else await tgupmsg.edit(STRINGS[lang]["ok_upload"].format(path.basename(doc_f), TimeFormatter(round(etm - stm))))
            # Cleanup
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
            return await self.answer_query(query, "Sorry! I can't find that file", True)
        except BaseException as e:
            logging.warn(e)
            await self.answer_query(query, f"**Error:** \n`{e}`")

    ######## Utils ########
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
                await query.message.delete()
            except:
                pass
            await self.send_message(query.message.chat.id, text, *args, **kwargs)
