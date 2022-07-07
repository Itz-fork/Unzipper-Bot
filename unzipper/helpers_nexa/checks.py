# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae


from pyrogram import enums
from config import Config
from unzipper import unzipperbot


def check_log_channel():
    try:
        if Config.LOGS_CHANNEL:
            c_info = unzipperbot.get_chat(chat_id=Config.LOGS_CHANNEL)
            if c_info.type != enums.ChatType.CHANNEL:
                return print("Chat is not a channel!")
            elif c_info.username is not None:
                return print("Chat is not private!")
            else:
                unzipperbot.send_message(
                    chat_id=Config.LOGS_CHANNEL, text="`Unzipper-Bot has Successfully Started!` \n\n**Powered by @NexaBotsUpdates**")
        else:
            print("No Log Channel ID is Given! Imma leaving Now!")
            exit()
    except:
        print("Error Happend while checking Log Channel! Make sure you're not dumb enough to provide a wrong Log Channel ID!")
