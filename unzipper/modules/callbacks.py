# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

import os
import re
import shutil
import aiofiles

from time import time
from aiohttp import ClientSession
from pyrogram import Client
from pyrogram.types import CallbackQuery

from .bot_data import Buttons, Messages, ERROR_MSGS
from .ext_script.ext_helper import extr_files, get_files, make_keyboard
from .ext_script.up_helper import send_file
from .commands import https_url_regex
from unzipper.helpers_nexa.unzip_help import progress_for_pyrogram, TimeFormatter, humanbytes
from config import Config

# Callbacks
@Client.on_callback_query()
async def unzipper_cb(unzip_bot: Client, query: CallbackQuery):
    if query.data == "megoinhome":
        await query.edit_message_text(text=Messages.START_TEXT.format(query.from_user.mention), reply_markup=Buttons.START_BUTTON)
    
    elif query.data == "helpcallback":
        await query.edit_message_text(text=Messages.HELP_TXT, reply_markup=Buttons.ME_GOIN_HOME)
    
    elif query.data == "aboutcallback":
        await query.edit_message_text(text=Messages.ABOUT_TXT, reply_markup=Buttons.ME_GOIN_HOME, disable_web_page_preview=True)
    
    elif query.data.startswith("extract_file"):
        user_id = query.from_user.id
        download_path = f"{Config.DOWNLOAD_LOCATION}/{user_id}"
        ext_files_dir = f"{download_path}/extracted"
        r_message = query.message.reply_to_message
        splitted_data = query.data.split("|")

        try:
            if splitted_data[1] == "url":
                url = r_message.text
                # Double check
                if not re.match(https_url_regex, url):
                    return await query.message.edit("`That's not a valid url 😑!`")
                s = ClientSession()
                async with s as ses:
                    unzip_head = await ses.head(url)
                    # Checks if url file size is bigger than 2GB (Telegram limit)
                    u_file_size = unzip_head.headers.get('content-length')
                    if u_file_size is None:
                        return await query.message.edit("`Sorry, An Error occurred while getting file size. Please try again after some time 🥺!`")
                    if Config.TG_MAX_SIZE < int(u_file_size):
                        return await query.message.edit("`File Size is too large to send in telegram 🥶!`")
                    unzip_resp = await ses.get(url)
                    # Checks if file is an archive using content-type header
                    if "application/" not in unzip_resp.headers.get('content-type'):
                        return await query.message.edit("`That's not an archive 😒!`")
                    if unzip_resp.status == 200:
                        # Makes download dir
                        os.makedirs(download_path)
                        # Send logs
                        await unzip_bot.send_message(chat_id=Config.LOGS_CHANNEL, text=Messages.LOG_TXT.format(user_id, url, u_file_size))
                        s_time = time()
                        u_file_with_ext = f"{download_path}/archive_from_{user_id}{os.path.splitext(url)[1]}"
                        await query.message.edit(f"**Trying to download!** \n\n**Url:** `{url}` \n\n`This may take a while, Go and grab a coffee ☕️!`")
                        file = await aiofiles.open(u_file_with_ext, mode="wb")
                        await file.write(await unzip_resp.read())
                        await file.close()
                        archive = u_file_with_ext
                        e_time = time()
                    else:
                        await query.message.edit("**Sorry I can't download that URL 🥺!**")
                        return
            
            elif splitted_data[1] == "tg_file":
                if r_message.document is None:
                    return await query.message.edit("`Give me an Archive to extract lamo!`")
                # Makes download dir
                os.makedirs(download_path)
                # Send Logs
                log_msg = await r_message.forward(chat_id=Config.LOGS_CHANNEL)
                await log_msg.reply(Messages.LOG_TXT.format(user_id, r_message.document.file_name, humanbytes(r_message.document.file_size)))
                s_time = time()
                archive = await r_message.download(
                    file_name=f"{download_path}/archive_from_{user_id}{os.path.splitext(r_message.document.file_name)[1]}",
                    progress=progress_for_pyrogram, progress_args=("**Trying to Download!** \n", query.message, s_time)
                    )
                e_time = time()
            else:
                await query.answer("Can't Find Details! Please contact support group!", show_alert=True)
            
            try:
                await query.message.edit(Messages.AFTER_OK_DL_TXT.format(TimeFormatter(round(e_time-s_time) * 1000)))
            except:
                await query.answer("Successfully Downloaded! Extracting Now 😊!", show_alert=True)
            


            if splitted_data[2] == "with_pass":
                password = await unzip_bot.ask(chat_id=query.message.chat.id ,text="**Please send me the password 🔑:**")
                ext_s_time = time()
                extractor = await extr_files(path=ext_files_dir, archive_path=archive, password=password.text)
                ext_e_time = time()
            else:
                ext_s_time = time()
                extractor = await extr_files(path=ext_files_dir, archive_path=archive)
                ext_e_time = time()
            # Checks if there is an error happend while extracting the archive
            if any(err in extractor for err in ERROR_MSGS):
                return await query.message.edit(Messages.EXT_FAILED_TXT)
            
            await query.message.edit(Messages.EXT_OK_TXT.format(TimeFormatter(round(ext_e_time-ext_s_time) * 1000)))
            
            
            # Upload extracted files
            paths = get_files(path=ext_files_dir)
            i_e_buttons = await make_keyboard(paths=paths, user_id=user_id, chat_id=query.message.chat.id)
            await query.message.edit("Select Files to Upload!", reply_markup=i_e_buttons)
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
        paths = get_files(path=file_path)
        # Next level logic lmao
        if not paths:
            if os.path.isdir(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"):
                shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            return await query.message.edit("`I've already sent you those files 😐, Don't ask me to resend 😒!`")
        
        await query.answer("Send that file to you. Please wait!")
        await send_file(unzip_bot=unzip_bot,
                        c_id=spl_data[2],
                        doc_f=paths[int(spl_data[3])],
                        query=query,
                        full_path=f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"
                    )

        # Refreshing Inline keyboard
        await query.message.edit("`Refreshing ⏳...`")
        rpaths = get_files(path=file_path)
        # There are no files let's die
        if not rpaths:
            try:
                shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            except:
                pass
            return await query.message.edit("`I've already sent you those files 😐, Don't ask me to resend 😒!`")
        i_e_buttons = await make_keyboard(paths=rpaths, user_id=query.from_user.id, chat_id=query.message.chat.id)
        await query.message.edit("Select Files to Upload!", reply_markup=i_e_buttons)
    
    
    elif query.data.startswith("ext_a"):
        spl_data = query.data.split("|")
        file_path = f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}/extracted"
        paths = get_files(path=file_path)
        if not paths:
            try:
                shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            except:
                pass
            return await query.message.edit("`I've already sent you those files 😐, Don't ask me to resend 😒!`")
        await query.answer("Trying to send all files to you. Please wait!")
        for file in paths:
            await send_file(unzip_bot=unzip_bot,
                            c_id=spl_data[2],
                            doc_f=file,
                            query=query,
                            full_path=f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"
                        )
        await query.message.edit("**Successfully Uploaded!** \n\n **Join @NexaBotsUpdates ❤️**")
        try:
            shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
        except Exception as e:
            await query.message.edit(Messages.ERROR_TXT.format(e))
    
    elif query.data == "cancel_dis":
        try:
            shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{query.from_user.id}")
            await query.message.edit(Messages.CANCELLED_TXT.format("Process Cancelled"))
        except:
            return await query.answer("There is nothing to remove lmao!", show_alert=True)
    
    elif query.data == "nobully":
        await query.message.edit("**Ok Ok! I won't delete those files 😂!**")
