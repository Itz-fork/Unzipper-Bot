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


from asyncio import get_event_loop
from unzipper.database.language import get_user_languages


USER_LANG = {}


def update_languages_cache():

    async def _iter_and_update():
        async for doc in await get_user_languages():
            USER_LANG[doc["_id"]] = doc["lang"]

    loop = get_event_loop()
    loop.run_until_complete(_iter_and_update())
