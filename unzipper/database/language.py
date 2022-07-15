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


lang_db = unzipper_db["languages_db"]


async def set_language(user_id: int, lang: str):
    exists = await lang_db.find_one({"_id": user_id})
    if exists:
        await lang_db.update_one({"_id": user_id}, {"$set": {"lang": lang}})
    else:
        await lang_db.insert_one({"_id": user_id, "lang": lang})


async def get_language(user_id: int):
    exists = await lang_db.find_one({"_id": user_id})
    if exists:
        return exists["lang"]
    else:
        return "en"