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

from os import makedirs, path
from config import Config
from .helpers_nexa.checks import check_log_channel
from pyrogram import idle


if __name__ == "__main__":
    if not path.isdir(Config.DOWNLOAD_LOCATION):
        makedirs(Config.DOWNLOAD_LOCATION)
    from . import unzip_client
    unzip_client.start()
    print("Checking Log Channel ...")
    check_log_channel()
    print("Bot is active Now! Join @NexaBotsUpdates")
    idle()
