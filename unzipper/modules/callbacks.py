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
from unzipper import unzip_client

from pyrogram.types import CallbackQuery
from unzipper.database.cloud import GofileDB
from unzipper.helpers_nexa.buttons import Buttons
from unzipper.database.upload_mode import set_upload_mode

from unzipper.helpers_nexa.utils import (TimeFormatter, get_files, humanbytes,
                                         progress_for_pyrogram)
from unzipper.database.split_arc import add_split_arc_user, del_split_arc_user
from unzipper.lib.downloader import Downloader
from unzipper.lib.backup_tool import CloudBackup
from unzipper.lib.extractor import Extractor, ExtractionFailed


# Callbacks
@unzip_client.on_callback_query()
async def unzipper_cb(unzipperbot, query: CallbackQuery):
    qdat = query.data

    if qdat == "megoinhome":
        await query.edit_message_text((await unzipperbot.get_string("start")).format(query.from_user.mention), reply_markup=Buttons.START)

    elif qdat == "helpcallback":
        await query.edit_message_text(await unzipperbot.get_string("help_head"), reply_markup=Buttons.HELP)

    elif qdat == "extracthelp":
        await query.edit_message_text(await unzipperbot.get_string("help_extract"), reply_markup=Buttons.HELP_BACK)

    elif qdat == "upmodhelp":
        await query.edit_message_text(await unzipperbot.get_string("help_upmode"), reply_markup=Buttons.HELP_BACK)

    elif qdat == "backuphelp":
        await query.edit_message_text(await unzipperbot.get_string("help_backup"), reply_markup=Buttons.HELP_BACK)

    elif qdat == "thumbhelp":
        await query.edit_message_text(await unzipperbot.get_string("help_thumb"), reply_markup=Buttons.HELP_BACK)

    elif qdat == "aboutcallback":
        await query.edit_message_text((await unzipperbot.get_string("about")).format(unzipperbot.version), reply_markup=Buttons.BACK, disable_web_page_preview=True)

    elif qdat.startswith("set_mode"):
        await set_upload_mode(query.from_user.id, qdat.split("|")[1])
        await unzipperbot.answer_query(query, (await unzipperbot.get_string("changed_upmode")).format(mode))

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
                    fsize = cleng if cleng else "undefined"
                    # Makes download dir
                    makedirs(download_path)
                    # Send logs
                    await unzipperbot.send_message(Config.LOGS_CHANNEL, (await unzipperbot.get_string("log")).format(user_id, url, fsize))
                s_time = time()
                arc_name = f"{download_path}/archive_from_{user_id}_{path.basename(url)}"
                await Downloader().from_direct_link(url, arc_name, query.message)
                e_time = time()

            elif splitted_data[1] == "tg_file":
                rdoc = r_message.document
                # Makes download dir
                makedirs(download_path)
                # Send Logs
                log_msg = await r_message.forward(Config.LOGS_CHANNEL)
                await log_msg.reply((await unzipperbot.get_string("log")).format(user_id, rdoc.file_name, humanbytes(rdoc.file_size)))
                s_time = time()
                arc_name = f"{download_path}/archive_from_{user_id}_{rdoc.file_name}"
                await r_message.download(
                    file_name=arc_name,
                    progress=progress_for_pyrogram, progress_args=(
                        "**Trying to Download!** \n", query.message, s_time)
                )
                e_time = time()

            else:
                return await unzipperbot.answer_query(query, "Can't Find Details! Please contact support group!", answer_only=True)

            await unzipperbot.answer_query(query, (await unzipperbot.get_string("ok_download")).format(arc_name, TimeFormatter(round(e_time-s_time) * 1000)))

            # Checks if the archive is a splitted one
            arc_ext = path.splitext(arc_name)[1]
            if arc_ext.replace(".", "").isnumeric():
                password = ""
                if splitted_data[2] == "with_pass":
                    password = (await unzipperbot.ask_user(query.message.chat.id, await unzipperbot.get_string("ask_password"))).text
                await unzipperbot.answer_query(query, await unzipperbot.get_string("alert_splitted_arc"))
                await add_split_arc_user(user_id, arc_name, password)
                return

            # Extract
            exter = Extractor()
            if splitted_data[2] == "with_pass":
                password = (await unzipperbot.ask_user(query.message.chat.id, await unzipperbot.get_string("ask_password"))).text
                ext_s_time = time()
                await exter.extract(arc_name, ext_files_dir, password.text)
                ext_e_time = time()
            else:
                ext_s_time = time()
                await exter.extract(arc_name, ext_files_dir)
                ext_e_time = time()

            await unzipperbot.answer_query(query, (await unzipperbot.get_string("ok_extract")).format(TimeFormatter(round(ext_e_time-ext_s_time) * 1000)))

            # Upload extracted files
            files = await get_files(path=ext_files_dir)
            i_e_buttons = await Buttons.make_keyboard(files, user_id, query.message.chat.id)
            await unzipperbot.answer_query(query, await unzipperbot.get_string("select_files"), reply_markup=i_e_buttons)

        except ExtractionFailed:
            await unzipperbot.answer_query(query, await unzipperbot.get_string("failed_extract"))
        except BaseException as e:
            try:
                await unzipperbot.answer_query(query, (await unzipperbot.get_string("failed_main")).format(e))
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
            return await unzipperbot.answer_query(query, await unzipperbot.get_string("alert_empty_files"))

        await unzipperbot.answer_query(query, await unzipperbot.get_string("alert_sending_file"))
        await unzipperbot.send_file(c_id=spl_data[2], doc_f=paths[int(spl_data[3])], query=query,)

        # Refreshing Inline keyboard
        await unzipperbot.answer_query(query, await unzipperbot.get_string("refreshing"))
        files = await get_files(file_path)
        # There are no files let's die
        if not files:
            try:
                rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            except:
                pass
            return await unzipperbot.answer_query(query, await unzipperbot.get_string("ok_upload"))
        i_e_buttons = await Buttons.make_keyboard(files, query.from_user.id, query.message.chat.id)
        await unzipperbot.answer_query(query, await unzipperbot.get_string("select_files"), reply_markup=i_e_buttons)

    elif qdat.startswith("ext_a"):
        spl_data = qdat.split("|")
        file_path = f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}/extracted"
        paths = await get_files(path=file_path)
        if not paths:
            if path.isdir(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"):
                rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            return await unzipperbot.answer_query(query, await unzipperbot.get_string("alert_empty_files"))

        await unzipperbot.answer_query(query, await unzipperbot.get_string("alert_sending_files"))
        for file in paths:
            await unzipperbot.send_file(spl_data[2], file, query)

        await unzipperbot.answer_query(query, await unzipperbot.get_string("ok_upload"))
        rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")

    elif qdat.startswith("gf_setting"):
        gf = GofileDB(query.from_user.id)
        mode = qdat.split("-")[1]
        if mode == "set":
            tkn = await unzipperbot.ask_user(query.message.chat.id, await unzipperbot.get_string("ask_gofile_token"))
            await gf.save_token(tkn.text)
            await tkn.delete()
        elif mode == "del":
            await gf.del_token()
        elif mode == "get":
            return await unzipperbot.answer_query(query, (await unzipperbot.get_string("gofile_token")).format(await gf.get_token()))
        await unzipperbot.answer_query(query, "**Done ✅!**")

    elif qdat.startswith("cloudbackup"):
        clb = CloudBackup(query.from_user.id)
        to = qdat.split("|")[1]
        if to == "gofile":
            await unzipperbot.answer_query(query, await unzipperbot.get_string("alert_uploading_to_gofile"))
            glnk = await clb.gofile_backup()
            await unzipperbot.answer_query(query, (await unzipperbot.get_string("ok_backup")).format(glnk), reply_markup=Buttons.make_button("Gofile link", url=glnk))

    elif qdat == "cancel_dis":
        await del_split_arc_user(query.from_user.id)
        rmtree(f"{Config.DOWNLOAD_LOCATION}/{query.from_user.id}")
        await unzipperbot.answer_query(query, (await unzipperbot.get_string("canceled")).format("Process cancelled"))

    elif qdat == "nobully":
        await unzipperbot.answer_query(query, await unzipperbot.get_string("ok_wont_delete"))
