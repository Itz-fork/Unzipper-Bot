# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from re import match
from time import time
from config import Config
from aiohttp import ClientSession
from pyrogram.types import Message
from aiofiles import open as openfile
from unzipper.helpers_nexa.utils import progress_for_pyrogram
from .errors import InvalidContentType, FileSizeNotFound, FileTooLarge, InvalidUrl, HttpStatusError


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

    async def from_direct_link(self, url: str, path: str, message: Message, udt: str = "**Trying to Download!** \n"):
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
                if not "application/" in resp.headers["Content-Type"]:
                    raise InvalidContentType
                # Handle content length header
                total = resp.headers["Content-Length"]
                if not total:
                    raise FileSizeNotFound
                # Raise FileTooLarge if the content size exceeds Config.MAX_DOWNLOAD_SIZE
                if total > Config.MAX_DOWNLOAD_SIZE:
                    raise FileTooLarge
                curr = 0
                st = time()
                async with openfile(path, mode="wb") as file:
                    async for chunk in resp.content.iter_chunked(Config.CHUNK_SIZE):
                        await file.write(chunk)
                        curr += len(chunk)
                        await progress_for_pyrogram(curr, total, udt, message, st)
