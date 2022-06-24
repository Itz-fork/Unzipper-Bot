# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

import os
from PIL import Image
from pyrogram.types import Message
from . import unzipper_db, unzipperbot, Config
from unzipper.helpers_nexa.unzip_help import run_cmds_on_cr


thumb_db = unzipper_db["thumbnails_db"]


async def download_thumbnail(mid):
    msg = await unzipperbot.get_messages(Config.DB_CHANNEL, mid)
    dmsg = await msg.download()
    return dmsg


def prepare_thumb(kw):
    ipath = kw["ipath"]
    tpath = f"{os.path.splitext(ipath)[0]}.thumb.jpg"
    with Image.open(ipath) as im:
        rim = im.convert("RGB")
        rim.thumbnail((320, 320))
        rim.save(tpath, "JPEG")
    return tpath


async def save_thumbnail(uid, message: Message):
    # Download the image
    ip = await message.download()
    thumb = await run_cmds_on_cr(prepare_thumb, ipath=ip)
    frwd_thumb = await unzipperbot.send_photo(Config.DB_CHANNEL, thumb)
    is_exist = await thumb_db.find_one({"_id": uid})
    if is_exist:
        await thumb_db.update_one({"_id": uid}, {"$set": {"path": frwd_thumb.id}})
    else:
        await thumb_db.insert_one({"_id": uid, "path": frwd_thumb.id})


async def get_thumbnail(user_id):
    gtm = await thumb_db.find_one({"_id": user_id})
    if gtm:
        return await download_thumbnail(gtm["path"])
    else:
        return None


async def del_thumbnail(user_id):
    is_exist = await thumb_db.find_one({"_id": user_id})
    if is_exist:
        await thumb_db.delete_one({"_id": user_id})
    else:
        return
