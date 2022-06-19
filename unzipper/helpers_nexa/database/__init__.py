# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from config import Config
from unzipper import unzipperbot
from motor.motor_asyncio import AsyncIOMotorClient

mongodb = AsyncIOMotorClient(Config.MONGODB_URL)
unzipper_db = mongodb["Unzipper_Bot"]
