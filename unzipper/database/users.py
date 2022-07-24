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

from . import unzipper_db


# Main users database
user_db = unzipper_db["users_db"]


async def add_user(user_id: int):
    is_exist = await user_db.find_one({"user_id": user_id})
    if not is_exist:
        await user_db.insert_one({"user_id": user_id})


async def del_user(user_id: int):
    is_exist = await user_db.find_one({"user_id": user_id})
    if is_exist:
        await user_db.delete_one({"user_id": user_id})


async def is_user_in_db(user_id: int):
    is_exist = await user_db.find_one({"user_id": user_id})
    return True if is_exist else False


async def count_users():
    return await user_db.count_documents({})


async def get_users_list():
    return (user["user_id"] async for user in user_db.find({}))


# Banned users database (I don't know why tf i added this, but who cares)
b_user_db = unzipper_db["banned_users_db"]


async def add_banned_user(user_id: int):
    is_exist = await b_user_db.find_one({"banned_user_id": user_id})
    if not is_exist:
        await b_user_db.insert_one({"banned_user_id": user_id})


async def del_banned_user(user_id: int):
    is_exist = await b_user_db.find_one({"banned_user_id": user_id})
    if is_exist:
        await b_user_db.delete_one({"banned_user_id": user_id})


async def is_user_in_bdb(user_id: int):
    is_exist = await b_user_db.find_one({"banned_user_id": user_id})
    return True if is_exist else False


async def count_banned_users():
    return await b_user_db.count_documents({})
