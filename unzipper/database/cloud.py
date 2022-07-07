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


# Gofile.io
class GofileDB:
    def __init__(self, id: int) -> None:
        self.id = id
        self.db = unzipper_db["gofile_db"]

    async def save_token(self, gtoken: str):
        is_exist = await self.db.find_one({"_id": self.id})
        if is_exist:
            await self.db.update_one({"_id": self.id}, {"$set": {"token": gtoken}})
        else:
            await self.db.insert_one({"_id": self.id, "token": gtoken})

    async def get_token(self):
        gtkn = await self.db.find_one({"_id": self.id})
        if gtkn:
            return gtkn["token"]
        else:
            return None

    async def del_token(self):
        is_exist = await self.db.find_one({"_id": self.id})
        if is_exist:
            await self.db.delete_one({"_id": self.id})
        else:
            return
