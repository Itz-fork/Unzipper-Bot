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


from pyrogram import enums
from config import Config
from unzipper import unzip_client


def check_log_channel():
    try:
        if Config.LOGS_CHANNEL:
            c_info = unzip_client.get_chat(chat_id=Config.LOGS_CHANNEL)
            if c_info.type != enums.ChatType.CHANNEL:
                return print("Chat is not a channel!")
            elif c_info.username is not None:
                return print("Chat is not private!")
            else:
                unzip_client.send_message(
                    chat_id=Config.LOGS_CHANNEL, text="`Unzipper-Bot has Successfully Started!` \n\n**Powered by @NexaBotsUpdates**")
        else:
            print("No Log Channel ID is Given! Imma leaving Now!")
            exit()
    except:
        print("Error Happend while checking Log Channel! Make sure you're not dumb enough to provide a wrong Log Channel ID!")
