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

spl_db = unzipper_db["splitted_archive_users"]


async def add_split_arc_user(uid: int, fn: str, passw: str):
    is_exist = await spl_db.find_one({"_id": uid})
    if not is_exist:
        await spl_db.insert_one({"_id": uid, "file_name": fn, "password": passw})
    else:
        raise ValueError("Data already exists!")


async def get_split_arc_user(uid: int):
    gsau = await spl_db.find_one({"_id": uid})
    if gsau:
        return True, gsau["file_name"], gsau["password"]
    else:
        return False, None, None


async def del_split_arc_user(uid: int):
    is_exist = await spl_db.find_one({"_id": uid})
    if is_exist:
        await spl_db.delete_one({"_id": uid})
    else:
        return
