# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

import os
import re
import shutil

from time import time
from config import Config
from pyrogram import Client
from aiohttp import ClientSession
from aiofiles import open as openfile
from pyrogram.types import CallbackQuery
from unzipper.helpers_nexa.database.cloud import GofileDB
from unzipper.helpers_nexa.database.upload_mode import set_upload_mode
from unzipper.helpers_nexa.unzip_help import (TimeFormatter, humanbytes,
                                              progress_for_pyrogram)
from unzipper.helpers_nexa.database.split_arc import add_split_arc_user, del_split_arc_user
from .backup import CloudBackup
from .commands import https_url_regex
from .bot_data import ERROR_MSGS, Buttons, Messages
from .ext_script.up_helper import answer_query, send_file
from .ext_script.ext_helper import extr_files, get_files, make_keyboard


# Function to download files from direct link using aiohttp
async def download(url, path):
    async with ClientSession() as session:
        async with session.get(url, timeout=None) as resp:
            async with openfile(path, mode="wb") as file:
                async for chunk in resp.content.iter_chunked(Config.CHUNK_SIZE):
                    await file.write(chunk)


# Callbacks
@Client.on_callback_query()
async def unzipper_cb(unzip_bot: Client, query: CallbackQuery):
    if query.data == "megoinhome":
        await query.edit_message_text(text=Messages.START_TEXT.format(query.from_user.mention), reply_markup=Buttons.START_BUTTON)

    elif query.data == "helpcallback":
        await query.edit_message_text(text=Messages.HELP_TXT, reply_markup=Buttons.HELP_BTNS)

    elif query.data == "extracthelp":
        await query.edit_message_text(text=Messages.EXTRACT_HELP, reply_markup=Buttons.HELP_MENU_BTN)

    elif query.data == "upmodhelp":
        await query.edit_message_text(text=Messages.UPMODE_HELP, reply_markup=Buttons.HELP_MENU_BTN)

    elif query.data == "backuphelp":
        await query.edit_message_text(text=Messages.BACKUP_HELP, reply_markup=Buttons.HELP_MENU_BTN)

    elif query.data == "thumbhelp":
        await query.edit_message_text(text=Messages.THUMB_HELP, reply_markup=Buttons.HELP_MENU_BTN)

    elif query.data == "aboutcallback":
        await query.edit_message_text(text=Messages.ABOUT_TXT, reply_markup=Buttons.ME_GOIN_HOME, disable_web_page_preview=True)
    elif query.data.startswith("set_mode"):
        user_id = query.from_user.id
        mode = query.data.split("|")[1]
        await set_upload_mode(user_id, mode)
        await answer_query(query, Messages.CHANGED_UPLOAD_MODE_TXT.format(mode))

    elif query.data.startswith("extract_file"):
        user_id = query.from_user.id
        download_path = f"{Config.DOWNLOAD_LOCATION}/{user_id}"
        ext_files_dir = f"{download_path}/extracted"
        r_message = query.message.reply_to_message
        splitted_data = query.data.split("|")

        try:
            arc_name = ""
            if splitted_data[1] == "url":
                url = r_message.text
                # Double check
                if not re.match(https_url_regex, url):
                    return await query.message.edit("`That's not a valid url 😑!`")
                s = ClientSession()
                async with s as ses:
                    # Get the file size
                    unzip_head = await ses.head(url)
                    f_size = unzip_head.headers.get('content-length')
                    u_file_size = f_size if f_size else "undefined"
                    # Checks if file is an archive using content-type header
                    unzip_resp = await ses.get(url, timeout=None)
                    if "application/" not in unzip_resp.headers.get('content-type'):
                        return await query.message.edit("`That's not an archive 😒!`")
                    if unzip_resp.status == 200:
                        # Makes download dir
                        os.makedirs(download_path)
                        # Send logs
                        await unzip_bot.send_message(chat_id=Config.LOGS_CHANNEL, text=Messages.LOG_TXT.format(user_id, url, u_file_size))
                        s_time = time()
                        arc_name = f"{download_path}/archive_from_{user_id}{os.path.splitext(url)[1]}"
                        await answer_query(query, f"**Trying to download!** \n\n**Url:** `{url}` \n\n`This may take a while, Go and grab a coffee ☕️!`", unzip_client=unzip_bot)
                        await download(url, arc_name)
                        e_time = time()
                    else:
                        return await query.message.edit("**Sorry I can't download that URL 🥺!**")

            elif splitted_data[1] == "tg_file":
                if r_message.document is None:
                    return await query.message.edit("`Give me an Archive to extract lmao!`")
                # Makes download dir
                os.makedirs(download_path)
                # Send Logs
                log_msg = await r_message.forward(chat_id=Config.LOGS_CHANNEL)
                await log_msg.reply(Messages.LOG_TXT.format(user_id, r_message.document.file_name, humanbytes(r_message.document.file_size)))
                s_time = time()
                arc_name = f"{download_path}/archive_from_{user_id}{os.path.splitext(r_message.document.file_name)[1]}"
                archive = await r_message.download(
                    file_name=arc_name,
                    progress=progress_for_pyrogram, progress_args=(
                        "**Trying to Download!** \n", query.message, s_time)
                )
                e_time = time()
            else:
                return await answer_query(query, "Can't Find Details! Please contact support group!", answer_only=True, unzip_client=unzip_bot)

            await answer_query(query, Messages.AFTER_OK_DL_TXT.format(TimeFormatter(round(e_time-s_time) * 1000)), unzip_client=unzip_bot)

            # Checks if the archive is a splitted one
            arc_ext = os.path.splitext(arc_name)[1]
            if arc_ext.replace(".", "").isnumeric():
                password = ""
                if splitted_data[2] == "with_pass":
                    password = (await unzip_bot.ask(chat_id=query.message.chat.id, text="**Please send me the password 🔑:**")).text
                await answer_query(query, Messages.SPLITTED_FILE_TXT)
                narc = f"splitted_archive_from_{user_id}{arc_ext}"
                os.rename(arc_name, narc)
                await add_split_arc_user(user_id, f"{download_path}/{narc}", password)
                return

            if splitted_data[2] == "with_pass":
                password = await unzip_bot.ask(chat_id=query.message.chat.id, text="**Please send me the password 🔑:**")
                ext_s_time = time()
                extractor = await extr_files(path=ext_files_dir, archive_path=archive, password=password.text)
                ext_e_time = time()
            else:
                ext_s_time = time()
                extractor = await extr_files(path=ext_files_dir, archive_path=archive)
                ext_e_time = time()
            # Checks if there is an error happend while extracting the archive
            if any(err in extractor for err in ERROR_MSGS):
                try:
                    return await query.message.edit(Messages.EXT_FAILED_TXT)
                except:
                    try:
                        await query.message.delete()
                    except:
                        pass
                    return await unzip_bot.send_message(chat_id=query.message.chat.id, text=Messages.EXT_FAILED_TXT)

            await answer_query(query, Messages.EXT_OK_TXT.format(TimeFormatter(round(ext_e_time-ext_s_time) * 1000)), unzip_client=unzip_bot)

            # Upload extracted files
            paths = await get_files(path=ext_files_dir)
            i_e_buttons = await make_keyboard(paths=paths, user_id=user_id, chat_id=query.message.chat.id)
            try:
                await query.message.edit("`Select Files to Upload!`", reply_markup=i_e_buttons)
            except:
                await unzip_bot.send_message(chat_id=query.message.chat.id, text="`Select Files to Upload!`", reply_markup=i_e_buttons)
                await query.message.delete()

        except Exception as e:
            try:
                await query.message.edit(Messages.ERROR_TXT.format(e))
                shutil.rmtree(download_path)
                await s.close()
            except Exception as er:
                print(er)

    elif query.data.startswith("ext_f"):
        spl_data = query.data.split("|")
        file_path = f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}/extracted"
        paths = await get_files(path=file_path)
        # Next level logic lmao
        if not paths:
            if os.path.isdir(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"):
                shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            return await query.message.edit("`I've already sent you those files 😐, Don't ask me to resend 😒!`")

        await query.answer("Sending that file to you. Please wait!")
        await send_file(c_id=spl_data[2],
                        doc_f=paths[int(spl_data[3])],
                        query=query,
                        full_path=f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"
                        )

        # Refreshing Inline keyboard
        await query.message.edit("`Refreshing ⏳...`")
        rpaths = await get_files(path=file_path)
        # There are no files let's die
        if not rpaths:
            try:
                shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            except:
                pass
            return await query.message.edit("**Successfully Uploaded!** \n\n **Join @NexaBotsUpdates ❤️**")
        i_e_buttons = await make_keyboard(paths=rpaths, user_id=query.from_user.id, chat_id=query.message.chat.id)
        await query.message.edit("Select Files to Upload!", reply_markup=i_e_buttons)

    elif query.data.startswith("ext_a"):
        spl_data = query.data.split("|")
        file_path = f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}/extracted"
        paths = await get_files(path=file_path)
        if not paths:
            try:
                shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            except:
                pass
            return await query.message.edit("`I've already sent you those files 😐, Don't ask me to resend 😒!`")
        await query.answer("Trying to send all files to you. Please wait!")
        for file in paths:
            await send_file(c_id=spl_data[2],
                            doc_f=file,
                            query=query,
                            full_path=f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"
                            )
        await query.message.edit("**Successfully Uploaded!** \n\n **Join @NexaBotsUpdates ❤️**")
        try:
            shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
        except Exception as e:
            await query.message.edit(Messages.ERROR_TXT.format(e))

    elif query.data.startswith("gf_setting"):
        gf = GofileDB(query.from_user.id)
        mode = query.data.split("-")[1]
        if mode == "set":
            tkn = await unzip_bot.ask(chat_id=query.message.chat.id, text="**Please send me your gofile.io token**")
            await gf.save_token(tkn)
            await tkn.delete()
        elif mode == "del":
            await gf.del_token()
        elif mode == "get":
            return await answer_query(query, "**Your gofile token:** `{}`".format(await gf.get_token()))
        await answer_query(query, "**Done ✅!**")

    elif query.data.startswith("cloudbackup"):
        try:
            clb = CloudBackup(query.from_user.id)
            to = query.data.split("|")[1]
            if to == "gofile":
                await answer_query(query, "`Uploading extracted files to gofile.io! Please wait...`")
                glnk = await clb.gofile_backup()
                await answer_query(query, Messages.BACKUP_OK_TXT.format(glnk), btns=Buttons.GOFILE_BTN(glnk))
        except Exception as e:
            await answer_query(query, e)

    elif query.data == "cancel_dis":
        try:
            await del_split_arc_user(query.from_user.id)
            shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{query.from_user.id}")
            await query.message.edit(Messages.CANCELLED_TXT.format("Process Cancelled"))
        except:
            return await query.answer("There is nothing to remove lmao!", show_alert=True)

    elif query.data == "nobully":
        await query.message.edit("**Ok Ok! I won't delete those files 😂!**")
