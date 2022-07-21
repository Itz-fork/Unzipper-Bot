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

from re import match
from time import time
from config import Config
from aiohttp import ClientSession
from pyrogram.types import Message
from aiofiles import open as openfile
from unzipper.helpers_nexa.utils import progress_for_pyrogram
from .errors import InvalidContentType, FileTooLarge, InvalidUrl, HttpStatusError


# Http/Https url regex
# Added as a seperate variable to import only regex pattern
dl_regex = ("((http|https)://)(www.)?" +
            "[a-zA-Z0-9@:%._\\+~#?&//=]" +
            "{2,256}\\.[a-z]" +
            "{2,6}\\b([-a-zA-Z0-9@:%" +
            "._\\+~#?&//=]*)")


class Downloader:
    """
    Download direct links
    """

    def __init__(self) -> None:
        self.dl_regex = ("((http|https)://)(www.)?" +
                         "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                         "{2,256}\\.[a-z]" +
                         "{2,6}\\b([-a-zA-Z0-9@:%" +
                         "._\\+~#?&//=]*)")

    async def from_direct_link(self, url: str, path: str, message: Message = None, cont_type: str = "application/", udt: str = "**Trying to Download!** \n"):
        """
        Download a file from direct link

        Parameters:

            - `url` - Url to the file
            - `path` - Output path
            - `message` - Pyrogram Message object
            - `udt` - Header for the progress bar
        """
        # Raise InvalidUrl if regex mismatches
        if not match(self.dl_regex, url):
            raise InvalidUrl

        async with ClientSession() as session:
            async with session.get(url, timeout=None) as resp:
                # Raise HttpStatusError if response status isn't 200
                if resp.status != 200:
                    raise HttpStatusError
                # Raise InvalidContentType if the content isn't an archive
                if not cont_type in resp.content_type:
                    raise InvalidContentType
                # Handle content length header
                total = resp.content_length
                # Raise FileTooLarge if the content size exceeds Config.MAX_DOWNLOAD_SIZE
                if total and int(total) > Config.MAX_DOWNLOAD_SIZE:
                    raise FileTooLarge
                curr = 0
                st = time()
                async with openfile(path, mode="wb") as file:
                    async for chunk in resp.content.iter_chunked(Config.CHUNK_SIZE):
                        # Raise FileTooLarge if the content size exceeds Config.MAX_DOWNLOAD_SIZE
                        if curr > Config.MAX_DOWNLOAD_SIZE:
                            raise FileTooLarge
                        await file.write(chunk)
                        curr += len(chunk)
                        if message:
                            await progress_for_pyrogram(curr, total, udt, message, st)
