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

from json import loads
from os.path import basename
from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Buttons:

    def get_text() -> dict:
        """
        Get the dict that contains the strings of buttons according to the saved language type
        """
        lang = "en"
        with open(f"unzipper/localization/{lang}/buttons.json") as ls:
            return loads(ls.read())

    async def make_button(text: str, *args, **kwargs):
        """
        Create pyrogram InlineKeyboardMarkup object with 1 button
        """
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text, *args, **kwargs)]
        ])

    async def make_keyboard(files: str, user_id: int, chat_id: int):
        texts = Buttons.get_text()
        i_kbd = InlineKeyboard(row_width=2)
        data = []
        data.append(
            InlineKeyboardButton(
                texts["upload_all"], f"ext_a|{user_id}|{chat_id}")
        )
        data.append(
            InlineKeyboardButton(texts["cancel"], "cancel_dis")
        )
        for num, file in enumerate(files):
            # Temp fix for REPLY_MARKUP_TOO_LONG error
            if num > 90:
                break
            data.append(
                InlineKeyboardButton(f"{num} - {basename(file)}".encode(
                    "utf-8").decode("utf-8"), f"ext_f|{user_id}|{chat_id}|{num}")
            )
        i_kbd.add(*data)
        return i_kbd

    texts = get_text()

    START = InlineKeyboardMarkup([[
        InlineKeyboardButton(texts["help"], callback_data="helpcallback"),
        InlineKeyboardButton(texts["about"], callback_data="aboutcallback")
    ]])

    HELP = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                texts["help_extract"], callback_data="extracthelp"),
            InlineKeyboardButton(
                texts["help_upload"], callback_data="upmodhelp")
        ],
        [
            InlineKeyboardButton(
                texts["help_thumbnail"], callback_data="thumbhelp"),
            InlineKeyboardButton(
                texts["help_backup"], callback_data="backuphelp")
        ],
        [
            InlineKeyboardButton(texts["back"], callback_data="megoinhome")
        ]
    ])

    HELP_BACK = InlineKeyboardMarkup(
        [[InlineKeyboardButton(texts["back_to_help_menu"], callback_data="helpcallback")]])

    EXTRACT_FILE = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                texts["extract_file"], callback_data="extract_file|tg_file|no_pass")
        ],
        [
            InlineKeyboardButton(
                texts["extract_file_pass"], callback_data="extract_file|tg_file|with_pass")
        ],
        [
            InlineKeyboardButton(texts["cancel"], callback_data="cancel_dis")
        ]
    ])

    EXTRACT_URL = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                texts["extract_url"], callback_data="extract_file|url|no_pass"),
        ],
        [
            InlineKeyboardButton(
                texts["extract_url_pass"], callback_data="extract_file|url|with_pass")
        ],
        [
            InlineKeyboardButton(texts["cancel"], callback_data="cancel_dis")
        ]
    ])

    CLEAN = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(texts["clean"], callback_data="cancel_dis")
        ],
        [
            InlineKeyboardButton(texts["no_cancel"], callback_data="nobully")
        ]
    ])

    BACKUP = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Gofile.io", callback_data="cloudbackup|gofile"), ]])

    SETTINGS_GOFILE = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                texts["gofile_set"], callback_data="gf_setting-set"),
            InlineKeyboardButton(
                texts["gofile_del"], callback_data="gf_setting-del")
        ],
        [
            InlineKeyboardButton(
                texts["gofile_get"], callback_data="gf_setting-get")
        ]
    ])

    UPLOAD_MODE = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(texts["as_doc"], callback_data="set_mode|doc")
        ],
        [
            InlineKeyboardButton(
                texts["as_vid"], callback_data="set_mode|video")
        ]
    ])

    BACK = InlineKeyboardMarkup(
        [[InlineKeyboardButton(texts["back"], callback_data="megoinhome")]])
