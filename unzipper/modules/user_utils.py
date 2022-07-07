# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from os import remove
from pyrogram import filters
from unzipper import unzipperbot
from pyrogram.types import Message
from unzipper.helpers_nexa.buttons import Buttons
from unzipper.database.thumbnail import save_thumbnail, get_thumbnail, del_thumbnail


@unzipperbot.on_message(filters.private & filters.command("start"))
@unzipperbot.handler_func
async def start_bot(_, message: Message):
    await message.reply_text((await unzipperbot.get_string("start")).format(message.from_user.mention), reply_markup=Buttons.START, disable_web_page_preview=True)


@unzipperbot.on_message(filters.private & filters.command(["save", "set_thumb"]))
@unzipperbot.handler_func
async def save_dis_thumb(_, message: Message):
    prs_msg = await message.reply(await unzipperbot.get_string("processing"), reply_to_message_id=message.id)
    rply = message.reply_to_message
    if not rply or not rply.photo:
        return await prs_msg.edit(await unzipperbot.get_string("no_replied_msg"))
    await save_thumbnail(message.from_user.id, rply)
    await prs_msg.edit(await unzipperbot.get_string("ok_saving_thumb"))


@unzipperbot.on_message(filters.private & filters.command(["thget", "get_thumb"]))
@unzipperbot.handler_func
async def give_my_thumb(_, message: Message):
    prs_msg = await message.reply(await unzipperbot.get_string("processing"), reply_to_message_id=message.id)
    gthumb = await get_thumbnail(message.from_user.id)
    if not gthumb:
        return await prs_msg.edit(await unzipperbot.get_string("no_thumb"))
    await prs_msg.delete()
    await message.reply_photo(gthumb)
    remove(gthumb)


@unzipperbot.on_message(filters.private & filters.command(["thdel", "del_thumb"]))
@unzipperbot.handler_func
async def delete_my_thumb(_, message: Message):
    prs_msg = await message.reply(await unzipperbot.get_string("processing"), reply_to_message_id=message.id)
    texist = await get_thumbnail(message.from_user.id)
    if not texist:
        return await prs_msg.edit(await unzipperbot.get_string("no_thumb"))
    await del_thumbnail(message.from_user.id)
    remove(texist)
    await prs_msg.edit(await unzipperbot.get_string("ok_deleting_thumb"))


@unzipperbot.on_message(filters.private & filters.command("backup"))
@unzipperbot.handler_func
async def do_backup_files(_, message: Message):
    prs_msg = await message.reply(await unzipperbot.get_string("processing"), reply_to_message_id=message.id)
    await prs_msg.edit(await unzipperbot.get_string("select_provider"), reply_markup=Buttons.BACKUP)


@unzipperbot.on_message(filters.private & filters.command("clean"))
@unzipperbot.handler_func
async def clean_ma_files(_, message: Message):
    prs_msg = await message.reply(await unzipperbot.get_string("processing"), reply_to_message_id=message.id)
    await prs_msg.edit(await unzipperbot.get_string("ask_clean"), reply_markup=Buttons.CLN_BTNS)
