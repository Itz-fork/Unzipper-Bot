# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

import os
import shutil

from time import time
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery

from .bot_data import Buttons, Messages
from .ext_script.ext_helper import extract_with_7z_helper, get_files, make_keyboard
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
        os.makedirs(download_path)

        try:
            r_message = query.message.reply_to_message
            # Send Logs
            log_msg = await r_message.forward(chat_id=Config.LOGS_CHANNEL)
            await log_msg.reply(Messages.LOG_TXT.format(user_id, r_message.document.file_name, humanbytes(r_message.document.file_size)))
            s_time = time()
            archive = await r_message.download(file_name=f"{download_path}/archive_from_{user_id}", progress=progress_for_pyrogram, progress_args=("**Trying to Download!** \n", query.message, s_time))
            e_time = time()
            await query.message.edit(Messages.AFTER_OK_DL_TXT.format(TimeFormatter(round(e_time-s_time) * 1000)))
            
            # Extracting process
            mode = query.data.split("|")
            if mode[1] == "with_pass":
                password = await unzip_bot.ask(chat_id=query.message.chat.id ,text="**Please send me the password 🔑:**")
                ext_s_time = time()
                extractor = await extract_with_7z_helper(path=ext_files_dir, archive_path=archive, password=password.text)
                ext_e_time = time()
            else:
                ext_s_time = time()
                extractor = await extract_with_7z_helper(path=ext_files_dir, archive_path=archive)
                ext_e_time = time()
            if "Error" in extractor:
                return await query.message.edit(Messages.EXT_FAILED_TXT)
            await query.message.edit(Messages.EXT_OK_TXT.format(TimeFormatter(round(ext_e_time-ext_s_time) * 1000)))

            # Upload extracted files
            paths = get_files(path=ext_files_dir)
            i_e_buttons = await make_keyboard(paths=paths, user_id=user_id, chat_id=query.message.chat.id)
            await query.message.edit("Select Files to Upload!", reply_markup=i_e_buttons)
        except Exception as e:
            try:
                shutil.rmtree(download_path)
            except Exception as e:
                print(e)
            await query.message.edit(Messages.ERROR_TXT.format(e))

    elif query.data.startswith("ext_f"):
        spl_data = query.data.split("|")
        file_path = f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}/extracted"
        paths = get_files(path=file_path)
        # Next level logic lmao
        if not paths:
            if os.path.isdir(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}"):
                shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
            return await query.message.edit("`I've already sent you those files 😐, Don't ask me to resend 😒!`")
        try:
            await unzip_bot.send_document(chat_id=spl_data[2], document=paths[int(spl_data[3])], caption="**Extracted by @NexaUnzipper_Bot**")
            os.remove(paths[int(spl_data[3])])
        except FileNotFoundError:
            await query.answer("Sorry! I can't find that file", show_alert=True)
        except BaseException:
            shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
        # Refreshing Inline keyboard
        await query.message.edit("`Refreshing ⏳...`")
        rpaths = get_files(path=file_path)
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
            await query.message.edit("`I've already sent you those files 😐, Don't ask me to resend 😒!`")
        for file in paths:
            await unzip_bot.send_document(chat_id=spl_data[2], document=file, caption="**Extracted by @NexaUnzipper_Bot**")
        await query.message.edit("**Successfully Uploaded!** \n\n **Join @NexaBotsUpdates ❤️**")
        try:
            shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{spl_data[1]}")
        except FileNotFoundError:
            pass
        except BaseException as e:
            await query.message.edit(Messages.ERROR_TXT.format(e))
    
    elif query.data == "cancel_dis":
        try:
            shutil.rmtree(f"{Config.DOWNLOAD_LOCATION}/{query.from_user.id}")
            await query.message.edit(Messages.CANCELLED_TXT.format("Process Cancelled"))
        except:
            return await query.answer("There is nothing to remove lmao!", show_alert=True)
    
    elif query.data == "nobully":
        await query.message.edit("**Ok Ok! I won't delete those files 😂!**")
