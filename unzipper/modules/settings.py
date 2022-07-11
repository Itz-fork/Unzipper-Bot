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
from unzipper import unzip_client
from pyrogram.types import Message

from unzipper.helpers_nexa.buttons import Buttons
from unzipper.database.upload_mode import get_upload_mode


@unzip_client.on_message(filters.private & filters.command(["gofile", "gfsets"]))
@unzip_client.handle_erros
async def gofile_settings(unzipperbot, message: Message):
    prs_msg = await message.reply(await unzipperbot.get_string("processing"), reply_to_message_id=message.id)
    await prs_msg.edit("**Gofile.io settings ⚙️**", reply_markup=Buttons.GOFILE_ST_BTNS)


@unzip_client.on_message(filters.private & filters.command(["mode", "setmode"]))
@unzip_client.handle_erros
async def set_up_mode_for_user(unzipperbot, message: Message):
    prs_msg = await message.reply(await unzipperbot.get_string("processing"), reply_to_message_id=message.id)
    upload_mode = await get_upload_mode(message.from_user.id)
    await prs_msg.edit((await unzipperbot.get_string("select_upmode")).format(upload_mode), reply_markup=Buttons.UPLOAD_MODE)
