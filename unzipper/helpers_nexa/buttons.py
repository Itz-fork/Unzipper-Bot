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

from os.path import basename
from pykeyboard import InlineKeyboard
from unzipper.client.caching import STRINGS
from unzipper.helpers_nexa.utils import read_json_sync
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Unzipper_Buttons:
    def __init__(self) -> None:
        pass

    async def make_button(self, text: str, *args, **kwargs):
        """
        Create pyrogram InlineKeyboardMarkup object with 1 button
        """
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text, *args, **kwargs)]
        ])

    async def make_files_keyboard(self, files: list, user_id: int, chat_id: int, inlude_files: bool = True):
        i_kbd = InlineKeyboard(row_width=2)
        data = [InlineKeyboardButton(STRINGS["buttons"]["upload_all"], f"ext_a|{user_id}|{chat_id}"), InlineKeyboardButton(
            STRINGS["buttons"]["cancel"], "cancel_dis")]
        if inlude_files:
            for num, file in enumerate(files):
                # Stop iterating if file count is 90
                if num >= 90:
                    break
                data.append(
                    InlineKeyboardButton(f"{num} - {basename(file)}".encode(
                        "utf-8").decode("utf-8"), f"ext_f|{user_id}|{chat_id}|{num}")
                )
        i_kbd.add(*data)
        return i_kbd

    START = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            STRINGS["buttons"]["help"], callback_data="helpcallback"),
        InlineKeyboardButton(
            STRINGS["buttons"]["about"], callback_data="aboutcallback")
    ]])

    HELP = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["help_extract"], callback_data="extracthelp"),
            InlineKeyboardButton(
                STRINGS["buttons"]["help_upload"], callback_data="upmodhelp")
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["help_thumbnail"], callback_data="thumbhelp"),
            InlineKeyboardButton(
                STRINGS["buttons"]["help_backup"], callback_data="backuphelp")
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["help_langs"], callback_data="langhelp")
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["back"], callback_data="megoinhome")
        ]
    ])

    HELP_BACK = InlineKeyboardMarkup(
        [[InlineKeyboardButton(STRINGS["buttons"]["back_to_help_menu"], callback_data="helpcallback")]])

    EXTRACT_FILE = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["extract_file"], callback_data="extract_file|tg_file|no_pass")
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["extract_file_pass"], callback_data="extract_file|tg_file|with_pass")
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["cancel"], callback_data="cancel_dis")
        ]
    ])

    EXTRACT_URL = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["extract_url"], callback_data="extract_file|url|no_pass"),
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["extract_url_pass"], callback_data="extract_file|url|with_pass")
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["cancel"], callback_data="cancel_dis")
        ]
    ])

    CLEAN = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["clean"], callback_data="cancel_dis")
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["no_cancel"], callback_data="nobully")
        ]
    ])

    BACKUP = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Gofile.io", callback_data="cloudbackup|gofile"), ]])

    SETTINGS_GOFILE = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["gofile_set"], callback_data="gf_setting-set"),
            InlineKeyboardButton(
                STRINGS["buttons"]["gofile_del"], callback_data="gf_setting-del")
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["gofile_get"], callback_data="gf_setting-get")
        ]
    ])

    UPLOAD_MODE = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["as_doc"], callback_data="set_mode|doc")
        ],
        [
            InlineKeyboardButton(
                STRINGS["buttons"]["as_vid"], callback_data="set_mode|video")
        ]
    ])

    LANGUAGES = InlineKeyboardMarkup([[InlineKeyboardButton(
        v, f"set_lang|{k}")] for k, v in read_json_sync("unzipper/localization/languages.json", True)])

    BACK = InlineKeyboardMarkup(
        [[InlineKeyboardButton(STRINGS["buttons"]["back"], callback_data="megoinhome")]])
