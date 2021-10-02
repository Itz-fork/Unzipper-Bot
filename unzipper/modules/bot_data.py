# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Inline buttons
class Buttons:
    START_BUTTON=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Help 📜", callback_data="helpcallback"),
                InlineKeyboardButton("About ⁉️", callback_data="aboutcallback")
            ]
        ]
    )
    
    CHOOSE_E_BTN=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Extract 📂", callback_data="extract_file|no_pass"),
                InlineKeyboardButton("(Password) Extract 📂", callback_data="extract_file|with_pass")
            ],
            [
                InlineKeyboardButton("Cancel ❌", callback_data="cancel_dis")
            ]
        ]
    )

    CLN_BTNS=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Clean My Files 😇", callback_data="cancel_dis")
            ],
            [
                InlineKeyboardButton("TF! Nooo 😳", callback_data="nobully")
            ]
        ]
    )
    
    ME_GOIN_HOME=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Back 🏡", callback_data="megoinhome")
            ]
        ]
    )


class Messages:
    START_TEXT = """
Hi **{}**, I'm **Nexa Unzipper Bot** 😇!

`I can extract archives like zip, rar, tar etc.`

**Made with ❤️ by @NexaBotsUpdates**
    """

    HELP_TXT = """
**How To Extract? 🤔**

`1. Send the file that you want to extract.`
`2. Click on extract button.`


**Note:**
    **1.** `If your archive is password protected select` **(Password) Extract 📂** `mode. Bot isn't a GOD to know your file's password so If this happens just send that password!`
    
    **2.** `Please don't send corrupted files! If you sent a one by a mistake just send` **/clean** `command!`
    """

    ABOUT_TXT = """
**About Nexa Unzipper Bot,**

✘ **Language:** [Python](https://www.python.org/)
✘ **Framework:** [Pyrogram](https://docs.pyrogram.org/)
✘ **Source Code:** `Soon...`
✘ **Developer:** [Itz-fork](https://github.com/Itz-fork)


**Made with ❤️ by @NexaBotsUpdates**
    """

    LOG_TXT = """
**Extract Log 📝!**

**User ID:** `{}`
**File Name:** `{}`
**File Size:** `{}`
    """

    AFTER_OK_DL_TXT = """
**Successfully Downloaded**

**Download time:** `{}`
**Status:** `Trying to extract the archive`
    """

    EXT_OK_TXT = """
**Extraction Successfull!**

**Extraction time:** `{}`
**Status:** `Trying to upload`
    """

    EXT_FAILED_TXT = """
**Extraction Failed 😕!**

**What to do?**

 - `Please make sure archive isn't corrupted`
 - `Please make sure that you selected the right mode!`
 - `May be Your archive format isn't supported 😔`

**Please report this at @Nexa_bots if you think this is a serious error**
    """

    ERROR_TXT = """
**Error Happend 😕!**

**ERROR:** {}


**Please report this at @Nexa_bots if you think this is a serious error**
    """

    CANCELLED_TXT = """
**{} ✅!**

`Now all of your files have been deleted from my server 😏!`
    """

    CLEAN_TXT = """
**Are sure want to delete your files from my server 🤔?**

**Note:** `This action cannot be undone!`
    """
