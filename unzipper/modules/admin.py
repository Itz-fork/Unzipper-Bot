# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from asyncio import sleep
from shutil import disk_usage as sdisk_usage

from config import Config
from pyrogram import filters
from unzipper import unzipperbot
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from unzipper.helpers_nexa.utils import humanbytes
from unzipper.database.users import (add_banned_user, count_banned_users,
                                     count_users, del_banned_user, del_user,
                                     get_users_list)
from psutil import cpu_percent, disk_usage, net_io_counters, virtual_memory


@unzipperbot.on_message(filters.private & filters.command("stats"))
async def send_stats(_, message: Message):
    stats_msg = await message.reply(await unzipperbot.get_string("processing"))
    # Is message from owner?
    frmow = False
    if message.from_user and message.from_user.id == Config.BOT_OWNER:
        frmow = True
    # Disk usage
    total, used, free = sdisk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    # Hardware usage
    cpu_usage = cpu_percent()
    ram_usage = virtual_memory().percent
    cdisk_usage = disk_usage('/').percent
    # Bandwith usage
    net_usage = net_io_counters()
    # Users count
    total_users = await count_users()
    total_banned_users = await count_banned_users()
    usrtxt = f"""
**👥 Users:** 
 ↳**Users in Database:** `{total_users}`
 ↳**Total Banned Users:** `{total_banned_users}`

"""
    # Show status
    await stats_msg.edit(f"""
**💫 Current Bot Stats 💫**
{usrtxt if frmow else ""}
**🌐 Bandwith Usage,**
 ↳ **Sent:** `{humanbytes(net_usage.bytes_sent)}`
 ↳ **Received:** `{humanbytes(net_usage.bytes_recv)}`


**💾 Disk Usage,**
 ↳**Total Disk Space:** `{total}`
 ↳**Used:** `{used}({cdisk_usage}%)`
 ↳**Free:** `{free}`


**🎛 Hardware Usage,**
 ↳**CPU Usage:** `{cpu_usage}%`
 ↳**RAM Usage:** `{ram_usage}%`""")


async def _do_broadcast(message, user):
    try:
        await message.copy(chat_id=int(user))
        return 200
    except FloodWait as e:
        await sleep(e.x)
        return _do_broadcast(message, user)
    except Exception:
        await del_user(user)


@unzipperbot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER))
async def broadcast_dis(_, message: Message):
    bc_msg = await message.reply(await unzipperbot.get_string("processing"))
    r_msg = message.reply_to_message
    if not r_msg:
        return await bc_msg.edit(await unzipperbot.get_string("no_replied_msg"))
    users_list = await get_users_list()
    # trying to broadcast
    await bc_msg.edit(await unzipperbot.get_string("broadcast_started"))
    success_no = 0
    failed_no = 0
    total_users = await count_users()
    for user in users_list:
        b_cast = await _do_broadcast(message=r_msg, user=user["user_id"])
        if b_cast == 200:
            success_no += 1
        else:
            failed_no += 1
    await bc_msg.edit((await unzipperbot.get_string("boradcast_results")).format(total_users, success_no, failed_no))


@unzipperbot.on_message(filters.private & filters.command("ban") & filters.user(Config.BOT_OWNER))
async def ban_user(_, message: Message):
    ban_msg = await message.reply(await unzipperbot.get_string("processing"))
    try:
        user_id = message.text.split(None, 1)[1]
    except:
        return await ban_msg.edit(await unzipperbot.get_string("no_userid"))
    await add_banned_user(user_id)
    await ban_msg.edit((await unzipperbot.get_string("ok_ban")).format(user_id))


@unzipperbot.on_message(filters.private & filters.command("unban") & filters.user(Config.BOT_OWNER))
async def unban_user(_, message: Message):
    unban_msg = await message.reply(await unzipperbot.get_string("processing"))
    try:
        user_id = message.text.split(None, 1)[1]
    except:
        return await unban_msg.edit(await unzipperbot.get_string("no_userid"))
    await del_banned_user(user_id)
    await unban_msg.edit((await unzipperbot.get_string("ok_unban")).format(user_id))
