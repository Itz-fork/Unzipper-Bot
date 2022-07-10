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
from pyrogram import idle
from os import makedirs, path
from unzipper.modules import *
from unzipper import unzip_client
from .helpers_nexa.checks import check_log_channel
from config import Config


# Logging stuff
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


if __name__ == "__main__":
    logging.info(" Copyright (c) 2022 Itz-fork ")

    logging.info(" >> Checking download location...")
    if not path.isdir(Config.DOWNLOAD_LOCATION):
        makedirs(Config.DOWNLOAD_LOCATION)

    logging.info(" >> Applying custom methods...")
    from .patch_client import patchit
    patchit()

    logging.info(" >> Starting client...")
    unzip_client.start()

    logging.info(" >> Checking Log Channel...")
    check_log_channel()

    logging.info("Bot is active Now! Join @NexaBotsUpdates")
    idle()
