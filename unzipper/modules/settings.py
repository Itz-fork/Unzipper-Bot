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

from pyrogram import filters
from pyrogram.types import Message
from unzipper import unzip_client, Buttons
from unzipper.database.language import get_language
from unzipper.database.upload_mode import get_upload_mode


@unzip_client.on_message(filters.private & filters.command(["gofile", "gfsets"]))
@unzip_client.handle_erros
async def gofile_settings(_, message: Message, texts):
    prs_msg = await message.reply(texts["processing"], reply_to_message_id=message.id)
    await prs_msg.edit("**Gofile.io settings ⚙️**", reply_markup=Buttons.SETTINGS_GOFILE)


@unzip_client.on_message(filters.private & filters.command(["mode", "setmode"]))
@unzip_client.handle_erros
async def set_up_mode_for_user(_, message: Message, texts):
    prs_msg = await message.reply(texts["processing"], reply_to_message_id=message.id)
    upload_mode = await get_upload_mode(message.from_user.id)
    await prs_msg.edit(texts["select_upmode"].format(upload_mode), reply_markup=Buttons.UPLOAD_MODE)


@unzip_client.on_message(filters.private & filters.command(["lang", "set_lang"]))
@unzip_client.handle_erros
async def language_settings(_, message: Message, texts):
    prs_msg = await message.reply(texts["processing"])
    clng = await get_language(message.from_user.id)
    await prs_msg.edit(texts["select_lang"].format(clng), reply_markup=Buttons.LANGUAGES)
