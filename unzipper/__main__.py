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

from pyrogram import idle
from . import unzipperbot
from os import path, makedirs
from .helpers_nexa.checks import check_log_channel
from config import Config

if __name__ == "__main__":
    if not path.isdir(Config.DOWNLOAD_LOCATION):
        makedirs(Config.DOWNLOAD_LOCATION)
    unzipperbot.start()
    print("Checking Log Channel ...")
    check_log_channel()
    print("Bot is active Now! Join @NexaBotsUpdates")
    idle()
