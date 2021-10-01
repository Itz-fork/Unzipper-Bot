# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

from pyrogram import Client
from pyromod import listen

from config import Config

plugins = dict(root="unzipper/modules")
unzipperbot = Client(
        "UnzipperBot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )