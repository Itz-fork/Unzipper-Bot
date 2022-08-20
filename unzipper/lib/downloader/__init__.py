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

from time import time
from re import match, sub
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
        self.gdrive_regex = r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=sharing"
        self.dl_regex = ("((http|https)://)(www.)?" +
                         "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                         "{2,256}\\.[a-z]" +
                         "{2,6}\\b([-a-zA-Z0-9@:%" +
                         "._\\+~#?&//=]*)")

    async def download(self, url: str, path: str, message: Message = None, redirect: bool = False, cont_type: str = "application/", udt: str = "**Trying to Download!** \n"):
        """
        Download a file from direct / gdrive link

        Parameters:

            - `url` - Url to the file
            - `path` - Output path
            - `message` - Pyrogram Message object
            - `redirect` - Redirect url
            - `udt` - Header for the progress bar
        """
        if match(self.gdrive_regex, url):
            gurl = await self._parse_gdrive(url)
            return await self._from_direct_link(url=gurl, path=path, message=message, redirect=True, cont_type=cont_type, udt=udt)
        elif match(self.dl_regex, url):
            return await self._from_direct_link(url=url, path=path, message=message, redirect=redirect, cont_type=cont_type, udt=udt)
        else:
            raise InvalidUrl

    async def _parse_gdrive(self, url: str):
        return sub(r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=sharing", r"https://drive.google.com/uc?export=download&id=\1", url)

    async def _from_direct_link(self, url: str, path: str, message: Message = None, redirect: bool = False, cont_type: str = "application/", udt: str = "**Trying to Download!** \n"):
        async with ClientSession() as session:
            async with session.get(url, timeout=None, allow_redirects=redirect) as resp:
                if resp.status == 200:
                    pass
                # Support for temporarily moved resources
                elif resp.status in (301, 302):
                    resp = await session.get(url, timeout=None, allow_redirects=True)
                # Raise HttpStatusError if response status isn't 200
                else:
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
