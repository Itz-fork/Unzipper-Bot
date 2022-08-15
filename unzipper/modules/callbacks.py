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
from shutil import rmtree
from os import makedirs, path

from config import Config
from aiohttp import ClientSession
from unzipper import unzip_client, Buttons
from unzipper.client.caching import USER_LANG

from pyrogram.types import CallbackQuery
from unzipper.database.cloud import GofileDB
from pyrogram.errors import ReplyMarkupTooLong
from unzipper.database.language import set_language
from unzipper.database.upload_mode import set_upload_mode

from unzipper.helpers_nexa.utils import (TimeFormatter, get_files, humanbytes,
                                         progress_for_pyrogram)
from unzipper.database.split_arc import add_split_arc_user, del_split_arc_user
from unzipper.lib.downloader import Downloader
from unzipper.lib.backup_tool import CloudBackup
from unzipper.lib.extractor import Extractor, ExtractionFailed


# Callbacks
@unzip_client.on_callback_query()
@unzip_client.handle_query
async def unzipper_cb(_, query: CallbackQuery, texts):
    qdat = query.data

    if qdat == "megoinhome":
        await query.edit_message_text(texts["start"].format(query.from_user.mention), reply_markup=Buttons.START)

    elif qdat == "helpcallback":
        await query.edit_message_text(texts["help_head"], reply_markup=Buttons.HELP)

    elif qdat == "extracthelp":
        await query.edit_message_text(texts["help_extract"], reply_markup=Buttons.HELP_BACK)

    elif qdat == "upmodhelp":
        await query.edit_message_text(texts["help_upmode"], reply_markup=Buttons.HELP_BACK)

    elif qdat == "backuphelp":
        await query.edit_message_text(texts["help_backup"], reply_markup=Buttons.HELP_BACK)

    elif qdat == "thumbhelp":
        await query.edit_message_text(texts["help_thumb"], reply_markup=Buttons.HELP_BACK)

    elif qdat == "langhelp":
        await query.edit_message_text(texts["help_lang"], reply_markup=Buttons.HELP_BACK)

    elif qdat == "aboutcallback":
        await query.edit_message_text(texts["about"].format(unzip_client.version), reply_markup=Buttons.BACK, disable_web_page_preview=True)

    elif qdat.startswith("extract_file"):
        splitted_data = qdat.split("|")
        user_id = query.from_user.id
        r_message = query.message.reply_to_message
        arc_name = ""
        download_path = f"{Config.DOWNLOAD_LOCATION}/{user_id}"
        ext_files_dir = f"{download_path}/extracted"

        try:
            if splitted_data[1] == "url":
                url = r_message.text
                async with ClientSession() as ses:
                    # Get the file size
                    cleng = (await ses.head(url)).headers.get("Content-Length")
                    fsize = humanbytes(int(cleng)) if cleng else "undefined"
                    # Makes download dir
                    makedirs(download_path)
                    # Send logs
                    await unzip_client.send_message(Config.LOGS_CHANNEL, texts["log"].format(user_id, "N/A", "N/A", url, fsize))
                s_time = time()
                arc_name = f"{download_path}/archive_from_{user_id}_{path.basename(url)}"
                await Downloader().download(url, arc_name, query.message)
                e_time = time()

            elif splitted_data[1] == "tg_file":
                # Makes download dir
                makedirs(download_path)
                # Send Logs
                rdoc = r_message.document
                rchat = r_message.forward_from_chat
                await r_message.copy(Config.LOGS_CHANNEL, texts["log"].format(
                    user_id,
                    rchat.title if rchat else "N/A",
                    rchat.id if rchat else "N/A",
                    rdoc.file_name,
                    humanbytes(rdoc.file_size))
                )
                s_time = time()
                arc_name = f"{download_path}/archive_from_{user_id}_{rdoc.file_name}"
                await r_message.download(
                    file_name=arc_name,
                    progress=progress_for_pyrogram, progress_args=(
                        "**Trying to Download!** \n", query.message, s_time)
                )
                e_time = time()

            else:
                return await unzip_client.answer_query(query, "Can't Find Details! Please contact support group!", answer_only=True)

            await unzip_client.answer_query(query, texts["ok_download"].format(arc_name, TimeFormatter(round(e_time-s_time) * 1000)))

            # Checks if the archive is a splitted one
            arc_ext = path.splitext(arc_name)[1]
            if arc_ext.replace(".", "").isnumeric():
                password = ""
                if splitted_data[2] == "with_pass":
                    password = (await unzip_client.ask(query.message.chat.id, texts["ask_password"])).text
                await unzip_client.answer_query(query, texts["alert_splitted_arc"])
                await add_split_arc_user(user_id, arc_name, password)
                return

            # Extract
            exter = Extractor()
            if splitted_data[2] == "with_pass":
                password = (await unzip_client.ask(query.message.chat.id, texts["ask_password"])).text
                ext_s_time = time()
                await exter.extract(arc_name, ext_files_dir, password)
                ext_e_time = time()
            else:
                ext_s_time = time()
                await exter.extract(arc_name, ext_files_dir)
                ext_e_time = time()

            await unzip_client.answer_query(query, texts["ok_extract"].format(TimeFormatter(round(ext_e_time-ext_s_time) * 1000)))

            # Upload extracted files
            files = await get_files(ext_files_dir)
            i_e_buttons = await Buttons.make_files_keyboard(files, user_id, query.message.chat.id)
            try:
                await unzip_client.answer_query(query, texts["select_files"], reply_markup=i_e_buttons)
            except ReplyMarkupTooLong:
                i_e_buttons = await Buttons.make_files_keyboard(files, user_id, query.message.chat.id, False)
                await unzip_client.answer_query(query, texts["select_files"], reply_markup=i_e_buttons)

        except ExtractionFailed:
            await unzip_client.answer_query(query, texts["failed_extract"])
        except BaseException as e:
            try:
                await unzip_client.answer_query(query, texts["failed_main"].format(e))
                rmtree(download_path)
            except Exception as er:
                logging.warn(er)

    elif qdat.startswith("ext_f"):
        spl_data = qdat.split("|")
        file_path = f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}/extracted"
        files = await get_files(file_path)
        # Next level logic lmao
        if not files:
            if path.isdir(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"):
                rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            return await unzip_client.answer_query(query, texts["alert_empty_files"])

        await unzip_client.answer_query(query, texts["alert_sending_file"], True)
        await unzip_client.send_file(spl_data[2], files[int(spl_data[3])], query, texts["this_lang"])

        # Refreshing Inline keyboard
        await unzip_client.answer_query(query, texts["refreshing"])
        files = await get_files(file_path)
        # There are no files let's die
        if not files:
            try:
                rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            except:
                pass
            return await unzip_client.answer_query(query, texts["ok_upload_basic"])
        i_e_buttons = await Buttons.make_files_keyboard(files, query.from_user.id, query.message.chat.id)
        try:
            await unzip_client.answer_query(query, texts["select_files"], reply_markup=i_e_buttons)
        except ReplyMarkupTooLong:
            i_e_buttons = await Buttons.make_files_keyboard(files, user_id, query.message.chat.id, False)
            await unzip_client.answer_query(query, texts["select_files"], reply_markup=i_e_buttons)

    elif qdat.startswith("ext_a"):
        spl_data = qdat.split("|")
        file_path = f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}/extracted"
        paths = await get_files(file_path)
        if not paths:
            if path.isdir(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"):
                rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            return await unzip_client.answer_query(query, texts["alert_empty_files"])

        await unzip_client.answer_query(query, texts["alert_sending_files"], True)
        for file in paths:
            await unzip_client.send_file(spl_data[2], file, query, texts["this_lang"], True)

        await unzip_client.answer_query(query, texts["ok_upload_basic"])
        rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")

    elif qdat.startswith("set_mode"):
        mode = qdat.split("|")[1]
        await set_upload_mode(query.from_user.id, mode)
        await unzip_client.answer_query(query, texts["changed_upmode"].format(mode))

    elif qdat.startswith("set_lang"):
        qlang = qdat.split("|")[1]
        chid = query.message.chat.id
        USER_LANG[chid] = qlang
        await set_language(chid, qlang)
        await unzip_client.answer_query(query, texts["changed_lang"].format(qlang))

    elif qdat.startswith("gf_setting"):
        gf = GofileDB(query.from_user.id)
        mode = qdat.split("-")[1]
        if mode == "set":
            tkn = await unzip_client.ask(query.message.chat.id, texts["ask_gofile_token"])
            await gf.save_token(tkn.text)
            await tkn.delete()
        elif mode == "del":
            await gf.del_token()
        elif mode == "get":
            return await unzip_client.answer_query(query, texts["gofile_token"].format(await gf.get_token()))
        await unzip_client.answer_query(query, "**Done ✅!**")

    elif qdat.startswith("cloudbackup"):
        clb = CloudBackup(query.from_user.id)
        to = qdat.split("|")[1]
        if to == "gofile":
            await unzip_client.answer_query(query, texts["alert_uploading_to_gofile"])
            glnk = await clb.gofile_backup()
            await unzip_client.answer_query(query, texts["ok_backup"].format(glnk), reply_markup=Buttons.make_button("Gofile link", url=glnk))

    elif qdat == "cancel_dis":
        await del_split_arc_user(query.from_user.id)
        try:
            rmtree(f"{Config.DOWNLOAD_LOCATION}/{query.from_user.id}")
        except:
            pass
        await unzip_client.answer_query(query, texts["canceled"].format("Process cancelled"))

    elif qdat == "nobully":
        await unzip_client.answer_query(query, texts["ok_wont_delete"])
