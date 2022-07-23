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
from json import loads
from asyncio import get_event_loop


# Cache dicts
USER_LANG = {}
STRINGS = {}


def update_languages_cache():
    from unzipper.database.language import get_user_languages

    async def _iter_and_update():
        async for doc in await get_user_languages():
            USER_LANG[doc["_id"]] = doc["lang"]

    loop = get_event_loop()
    loop.run_until_complete(_iter_and_update())


def update_text_strings():
    def _read_json(file, as_items=False):
        with open(file) as f:
            return loads(f.read()).items() if as_items else loads(f.read())

    subfolders = _read_json("unzipper/localization/languages.json", True)
    for lcode, fnm in subfolders:
        str_list = _read_json(f"unzipper/localization/{lcode}/messages.json")
        btn_strs = _read_json(f"unzipper/localization/defaults/buttons.json")
        STRINGS[lcode] = str_list
        STRINGS["buttons"] = btn_strs


def update_cache():
    logging.info(" >> Updating text strings cache...")
    update_text_strings()

    logging.info(" >> Updating language cache...")
    update_languages_cache()
