# ===================================================================== #
#                      Copyright (c) 2022 Itz-fork                      #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  #
# See the GNU General Public License for more details.                  #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>   #
# ===================================================================== #

import logging
from unzipper import unzip_client
from . import unzipper_db, Config

user_db = unzipper_db["users_db"]


async def add_user(user_id: int):
    is_exist = await user_db.find_one({"user_id": user_id})
    if is_exist:
        return
    else:
        await user_db.insert_one({"user_id": user_id})


async def del_user(user_id: int):
    is_exist = await user_db.find_one({"user_id": user_id})
    if is_exist:
        await user_db.delete_one({"user_id": user_id})
    else:
        return


async def is_user_in_db(user_id: int):
    is_exist = await user_db.find_one({"user_id": user_id})
    if is_exist:
        return True
    else:
        return False


async def count_users():
    return await user_db.count_documents({})


async def get_users_list():
    async for user in user_db.find({}):
        yield user["user_id"]


# Banned users database (I don't know why tf i added this, but who cares)
b_user_db = unzipper_db["banned_users_db"]


async def add_banned_user(user_id: int):
    is_exist = await b_user_db.find_one({"banned_user_id": user_id})
    if is_exist:
        return
    else:
        await b_user_db.insert_one({"banned_user_id": user_id})


async def del_banned_user(user_id: int):
    is_exist = await b_user_db.find_one({"banned_user_id": user_id})
    if is_exist:
        await b_user_db.delete_one({"banned_user_id": user_id})
    else:
        return


async def is_user_in_bdb(user_id: int):
    is_exist = await b_user_db.find_one({"banned_user_id": user_id})
    if is_exist:
        return True
    else:
        return False


async def count_banned_users():
    return await b_user_db.count_documents({})


async def get_banned_users_list():
    return [banned_users_list async for banned_users_list in b_user_db.find({})]


# Questioning about the user's existence on this planet
class MFYouAreBanned(Exception):
    def __init__(self) -> None:
        super().__init__("Mf you are banned from using this bot!")

async def check_user(message):
    # Checking if user is banned
    is_banned = await is_user_in_bdb(int(message.from_user.id))
    if is_banned:
        await message.reply("**Sorry You're Banned!** \n\nReport this at @Nexa_bots if you think this is a mistake")
        raise MFYouAreBanned
    # Chacking if user already in db
    is_in_db = await is_user_in_db(int(message.from_user.id))
    if not is_in_db:
        try:
            await add_user(int(message.from_user.id))
            await unzip_client.send_message(
                chat_id=Config.LOGS_CHANNEL,
                text=f"**#NEW_USER** 🎙 \n\n**User Profile:** `{message.from_user.mention}` \n**User ID:** `{message.from_user.id}` \n**Profile Url:** [Click here](tg://user?id={message.from_user.id})",
                disable_web_page_preview=True
            )
        except Exception as e:
            logging.warn(f"Unable to add user to the database due to: \n{e}")
