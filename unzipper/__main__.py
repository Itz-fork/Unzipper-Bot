# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

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
