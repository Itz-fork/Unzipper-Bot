# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from . import unzipper_db

mode_db = unzipper_db["upload_mode_db"]


async def set_upload_mode(user_id, mode):
    is_exist = await mode_db.find_one({"_id": user_id})
    if is_exist:
        await mode_db.update_one({"_id": user_id}, {"$set": {"mode": mode}})
    else:
        await mode_db.insert_one({"_id": user_id, "mode": mode})


async def get_upload_mode(user_id):
    umode = await mode_db.find_one({"_id": user_id})
    if umode:
        return umode["mode"]
    else:
        return "doc"
