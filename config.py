# Copyright (c) 2021 Itz-fork

import os

class Config(object):
    APP_ID = int(os.environ.get("APP_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    LOGS_CHANNEL = int(os.environ.get("LOGS_CHANNEL"))
    MONGODB_URL = os.environ.get("MONGODB_URL")
    BOT_OWNER = int(os.environ.get("BOT_OWNER"))
    DOWNLOAD_LOCATION = f"{os.path.dirname(__file__)}/NexaBots"
    TG_MAX_SIZE = 2040108421
