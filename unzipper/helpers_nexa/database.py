# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae
from unzipper import unzipperbot as Client
from motor.motor_asyncio import AsyncIOMotorClient

from config import Config

mongodb = AsyncIOMotorClient(Config.MONGODB_URL)
unzipper_db = mongodb["Unzipper_Bot"]

# Users Database
user_db = unzipper_db["users_db"]

async def add_user(user_id):
    new_user_id = int(user_id)
    is_exist = await user_db.find_one({"user_id": new_user_id})
    if is_exist:
        return
    else:
        await user_db.insert_one({"user_id": new_user_id})

async def del_user(user_id):
    del_user_id = int(user_id)
    is_exist = await user_db.find_one({"user_id": del_user_id})
    if is_exist:
        await user_db.delete_one({"user_id": del_user_id})
    else:
        return

async def is_user_in_db(user_id):
    u_id = int(user_id)
    is_exist = await user_db.find_one({"user_id": u_id})
    if is_exist:
        return True
    else:
        return False

async def count_users():
    users = await user_db.count_documents({})
    return users

async def get_users_list():
    return [users_list async for users_list in user_db.find({})]


# Banned users database (I don't know why tf i added this, but who cares)
b_user_db = unzipper_db["banned_users_db"]

async def add_banned_user(user_id):
    new_user_id = int(user_id)
    is_exist = await b_user_db.find_one({"banned_user_id": new_user_id})
    if is_exist:
        return
    else:
        await b_user_db.insert_one({"banned_user_id": new_user_id})

async def del_banned_user(user_id):
    del_user_id = int(user_id)
    is_exist = await b_user_db.find_one({"banned_user_id": del_user_id})
    if is_exist:
        await b_user_db.delete_one({"banned_user_id": del_user_id})
    else:
        return

async def is_user_in_bdb(user_id):
    u_id = int(user_id)
    is_exist = await b_user_db.find_one({"banned_user_id": u_id})
    if is_exist:
        return True
    else:
        return False

async def count_banned_users():
    users = await b_user_db.count_documents({})
    return users

async def get_banned_users_list():
    return [banned_users_list async for banned_users_list in b_user_db.find({})]

# Gonna Cry?
async def check_user(message):
    # Checking if user is banned
    is_banned = await is_user_in_bdb(message.from_user.id)
    if is_banned:
        await message.reply("**Sorry You're Banned!** \n\nReport this at @Nexa_bots if you think this is a mistake")
        await message.stop_propagation()
        return
    # Chacking if user already in db
    is_in_db = await is_user_in_db(message.from_user.id)
    if not is_in_db:
        await add_user(message.from_user.id)
        await Client.send_message(
            chat_id=Config.LOGS_CHANNEL,
            text=f"**#NEW_USER** 🎙 \n\n**User Profile:** `{message.from_user.mention}` \n**User ID:** `{message.from_user.id}` \n**Profile Url:** tg://user?id={message.from_user.id}",
            disable_web_page_preview=True
        )
    await message.continue_propagation()
