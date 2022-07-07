# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from pyrogram import filters
from unzipper import unzipperbot
from pyrogram.types import Message
from unzipper.helpers_nexa.buttons import Buttons
from unzipper.database.upload_mode import get_upload_mode


@unzipperbot.on_message(filters.private & filters.command(["gofile", "gfsets"]))
async def gofile_settings(_, message: Message):
    prs_msg = await message.reply(await unzipperbot.get_string("processing"), reply_to_message_id=message.id)
    await prs_msg.edit("**Gofile.io settings ⚙️**", reply_markup=Buttons.GOFILE_ST_BTNS)


@unzipperbot.on_message(filters.private & filters.command(["mode", "setmode"]))
async def set_up_mode_for_user(_, message: Message):
    prs_msg = await message.reply(await unzipperbot.get_string("processing"), reply_to_message_id=message.id)
    upload_mode = await get_upload_mode(message.from_user.id)
    await prs_msg.edit((await unzipperbot.get_string("select_upmode")).format(upload_mode), reply_markup=Buttons.UPLOAD_MODE)
