# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from time import strftime
from config import Config
from gofile2 import Async_Gofile
from .ext_script.ext_helper import get_files
from unzipper.helpers_nexa.database.cloud import GofileDB


class CloudBackup:
    """
    ### About

    Utility class to backup extracted files to cloud

    ### Arguments

        - `id` - User id
    """

    def __init__(self, id: int) -> None:
        self.id = id
        self.ext_dir = f"{Config.DOWNLOAD_LOCATION}/{self.id}/extracted"

    # Gofile
    async def gofile_backup(self):
        """
        Backup files to gofile.io
        """
        # Gofile client
        gf = Async_Gofile(await self._get_gofile_token())
        gf_id = await self._create_gofile_folder(gf)
        links = await gf.upload_folder(self.ext_dir, gf_id)
        return links[0]["downloadPage"]

    async def _create_gofile_folder(self, client: Async_Gofile):
        rtfid = (await client.get_Account())["rootFolder"]
        cf = await client.create_folder(rtfid, "Backup of {} in {}".format(self.id, strftime("%b %d, %Y %l:%M%p")))
        return cf["id"]

    async def _get_gofile_token(self):
        gdb = GofileDB(self.id)
        gt = await gdb.get_token()
        return gt if gt else Config.GOFILE_TOKEN
