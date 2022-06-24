# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae
import os
import re
import shutil
import psutil
import asyncio

from config import Config
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from unzipper.helpers_nexa.database.users import (add_banned_user,  # Banned Users db
                                                  check_user, get_users_list,
                                                  count_users, count_banned_users,
                                                  del_user, del_banned_user)
from unzipper.helpers_nexa.database.thumbnail import save_thumbnail, get_thumbnail, del_thumbnail
from unzipper.helpers_nexa.database.upload_mode import get_upload_mode
from unzipper.helpers_nexa.unzip_help import humanbytes
from .bot_data import Buttons, Messages

# Regex for http/https urls
https_url_regex = ("((http|https)://)(www.)?" +
                   "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                   "{2,256}\\.[a-z]" +
                   "{2,6}\\b([-a-zA-Z0-9@:%" +
                   "._\\+~#?&//=]*)")

# Function to check user status (is banned or not)


@Client.on_message(filters.private)
async def _(_, message: Message):
    await check_user(message)


@Client.on_message(filters.private & filters.command("start"))
async def start_bot(_, message: Message):
    await message.reply_text(text=Messages.START_TEXT.format(message.from_user.mention), reply_markup=Buttons.START_BUTTON, disable_web_page_preview=True)


@Client.on_message(filters.private & filters.command("clean"))
async def clean_ma_files(_, message: Message):
    await message.reply_text(text=Messages.CLEAN_TXT, reply_markup=Buttons.CLN_BTNS)


@Client.on_message(filters.incoming & filters.private & filters.regex(https_url_regex) | filters.document)
async def extract_dis_archive(_, message: Message):
    unzip_msg = await message.reply("`Processing ⚙️...`", reply_to_message_id=message.id)
    # Due to https://t.me/Nexa_bots/38823
    if not message.from_user:
        return await unzip_msg.edit("`Ayo, you ain't a user 🤨?")
    user_id = message.from_user.id
    download_path = f"{Config.DOWNLOAD_LOCATION}/{user_id}"
    if os.path.isdir(download_path):
        return await unzip_msg.edit("`Already one process is going on, Don't spam you idiot 😑!` \n\nWanna Clear You Files from my server? Then just send **/clean** command!")
    if message.text and (re.match(https_url_regex, message.text)):
        await unzip_msg.edit("**What do you want?**", reply_markup=Buttons.CHOOSE_E_U__BTNS)
    elif message.document:
        await unzip_msg.edit("**What do you want?**", reply_markup=Buttons.CHOOSE_E_F__BTNS)
    else:
        await unzip_msg.edit("`Hold up! What Should I Extract 😳?`")


# Thumbnail stuff
@Client.on_message(filters.private & filters.command(["save", "set_thumb"]))
async def save_dis_thumb(_, message: Message):
    prs_msg = await message.reply("`Processing ⚙️...`", reply_to_message_id=message.id)
    rply = message.reply_to_message
    if not rply or not rply.photo:
        return await prs_msg.edit("`Reply to an image file to save it as a thumbnail!`")
    await save_thumbnail(message.from_user.id, rply)
    await prs_msg.edit("**Successfully saved the thumbnail ✅!**")


@Client.on_message(filters.private & filters.command(["thget", "get_thumb"]))
async def give_my_thumb(_, message: Message):
    prs_msg = await message.reply("`Processing ⚙️...`", reply_to_message_id=message.id)
    gthumb = await get_thumbnail(message.from_user.id)
    if not gthumb:
        return await prs_msg.edit("No thumbnails found. Please set one using `/set_thumb` command!")
    await prs_msg.delete()
    await message.reply_photo(gthumb)
    os.remove(gthumb)


@Client.on_message(filters.private & filters.command(["thdel", "del_thumb"]))
async def delete_my_thumb(_, message: Message):
    prs_msg = await message.reply("`Processing ⚙️...`", reply_to_message_id=message.id)
    texist = await get_thumbnail(message.from_user.id)
    if not texist:
        return await prs_msg.edit("`When saving a thumbnail?`")
    await del_thumbnail(message.from_user.id)
    os.remove(texist)
    await prs_msg.edit("**Successfully deleted the thumbnail ✅!**")


# Database Commands
@Client.on_message(filters.private & filters.command(["mode", "setmode"]))
async def set_up_mode_for_user(_, message: Message):
    upload_mode = await get_upload_mode(message.from_user.id)
    await message.reply(Messages.SELECT_UPLOAD_MODE_TXT.format(upload_mode), reply_markup=Buttons.SET_UPLOAD_MODE_BUTTONS)


@Client.on_message(filters.private & filters.command("stats") & filters.user(Config.BOT_OWNER))
async def send_stats(_, message: Message):
    stats_msg = await message.reply("`Processing ⚙️...`")
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    net_usage = psutil.net_io_counters()
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await count_users()
    total_banned_users = await count_banned_users()
    await stats_msg.edit(f"""
**💫 Current Bot Stats 💫**

**👥 Users:** 
 ↳**Users in Database:** `{total_users}`
 ↳**Total Banned Users:** `{total_banned_users}`


**🌐 Bandwith Usage,**
 ↳ **Sent:** `{humanbytes(net_usage.bytes_sent)}`
 ↳ **Received:** `{humanbytes(net_usage.bytes_recv)}`


**💾 Disk Usage,**
 ↳**Total Disk Space:** `{total}`
 ↳**Used:** `{used}({disk_usage}%)`
 ↳**Free:** `{free}`


**🎛 Hardware Usage,**
 ↳**CPU Usage:** `{cpu_usage}%`
 ↳**RAM Usage:** `{ram_usage}%`"""
                         )


async def _do_broadcast(message, user):
    try:
        await message.copy(chat_id=int(user))
        return 200
    except FloodWait as e:
        asyncio.sleep(e.x)
        return _do_broadcast(message, user)
    except Exception:
        await del_user(user)


@Client.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER))
async def broadcast_dis(_, message: Message):
    bc_msg = await message.reply("`Processing ⚙️...`")
    r_msg = message.reply_to_message
    if not r_msg:
        return await bc_msg.edit("`Reply to a message to broadcast!`")
    users_list = await get_users_list()
    # trying to broadcast
    await bc_msg.edit("`Broadcasting has started, This may take while 🥱!`")
    success_no = 0
    failed_no = 0
    total_users = await count_users()
    for user in users_list:
        b_cast = await _do_broadcast(message=r_msg, user=user["user_id"])
        if b_cast == 200:
            success_no += 1
        else:
            failed_no += 1
    await bc_msg.edit(f"""
**Broadcast Completed ✅!**

**Total Users:** `{total_users}`
**Successful Responses:** `{success_no}`
**Failed Responses:** `{failed_no}`
    """)


@Client.on_message(filters.private & filters.command("ban") & filters.user(Config.BOT_OWNER))
async def ban_user(_, message: Message):
    ban_msg = await message.reply("`Processing ⚙️...`")
    try:
        user_id = message.text.split(None, 1)[1]
    except:
        return await ban_msg.edit("`Give a user id to ban!`")
    await add_banned_user(user_id)
    await ban_msg.edit(f"**Successfully Banned That User ✅** \n\n**User ID:** `{user_id}`")


@Client.on_message(filters.private & filters.command("unban") & filters.user(Config.BOT_OWNER))
async def unban_user(_, message: Message):
    unban_msg = await message.reply("`Processing ⚙️...`")
    try:
        user_id = message.text.split(None, 1)[1]
    except:
        return await unban_msg.edit("`Give a user id to unban!`")
    await del_banned_user(user_id)
    await unban_msg.edit(f"**Successfully Unbanned That User ✅** \n\n**User ID:** `{user_id}`")
